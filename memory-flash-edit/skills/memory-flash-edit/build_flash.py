# 回忆快闪工程档生成器（输出网页剪辑 .dvedit 的 project JSON，交 update_video_edit 写回）
# 用法：
#   python3 build_flash.py photos.json out.json            ← 只出最终工程
#   python3 build_flash.py photos.json out.json --steps D  ← 另出录屏用的逐步工程 D/p01.json…p13.json
#   --fast  改出「30 张快闪」变体（第一张 1.5 秒，其余每张 0.2 秒，放大 1.35＋手持晃动）
#   --ratio 9:16   画面比例（缺省 fit＝跟素材）
#   --music <云盘档 id> [--music-name 名字]  加一条配乐轨，从 0 起铺满全片
# photos.json：[{"name":"01.jpg","driveId":"<云盘档 id>"}, …]（照片先放进堤麟云端硬碟拿 id）
import json,sys,os,argparse
ap=argparse.ArgumentParser(); ap.add_argument('photos'); ap.add_argument('out')
ap.add_argument('--steps'); ap.add_argument('--fast',action='store_true'); ap.add_argument('--ratio')
ap.add_argument('--each',type=float,default=1.0)        # 每张时长
ap.add_argument('--zoom',type=float,default=1.08)       # 开头放大倍数（原教程 108）
ap.add_argument('--fx',default='fx-soft_bloom'); ap.add_argument('--fxs',type=float,default=1.0)
ap.add_argument('--tr',default='tr-flash_dissolve'); ap.add_argument('--trlen',type=float,default=0.4667)
ap.add_argument('--fin',type=float,default=0.27); ap.add_argument('--fout',type=float,default=0.33)
ap.add_argument('--music',help='配乐的云盘档 id（加一条音频轨，从 0 起铺满全片）'); ap.add_argument('--music-name',default='配乐.mp3')
a=ap.parse_args()
P=json.load(open(a.photos,encoding='utf-8')); N=len(P)
media=[{"id":f"m{i+1:02d}","name":p["name"],"kind":"image","duration":3,"from":"drive","driveId":p["driveId"]} for i,p in enumerate(P)]
ratio={"kind":"preset","key":a.ratio} if a.ratio else {"kind":"fit"}
def proj(clips,med,music=False):
  tr=[{"id":"main","kind":"visual","clips":clips,"locked":False,"hidden":False,"muted":False}]
  if music and a.music and clips:   # 配乐轨放 main 下面，从 0 起铺满全片，尾巴淡出 1 秒
    end=round(max(c["start"]+c["length"] for c in clips),4)
    med=med+[{"id":"mbgm","name":a.music_name,"kind":"audio","duration":0,"from":"drive","driveId":a.music}]
    tr.append({"id":"bgm","kind":"audio","clips":[{"id":"bgm1","mediaId":"mbgm","start":0,"length":end,"offset":0,"fadeOut":1}],"locked":False,"hidden":False,"muted":False})
  return {"v":1,"ratio":ratio,"tracks":tr,"media":med,"programs":{}}
def kf(z,end,ease=True):
  k0={"t":0,"v":z}; 
  if ease: k0["e"]="out"
  return {"sx":[dict(k0),{"t":end,"v":1}],"sy":[dict(k0),{"t":end,"v":1}]}
if a.fast:
  clips=[]; t=0
  for i in range(N):
    L=1.5 if i==0 else 0.2; z=1.25 if i==0 else 1.35
    c={"id":f"c{i+1:02d}","mediaId":f"m{i+1:02d}","start":round(t,4),"length":L,"offset":0,"kf":kf(z,L)}
    if i: c["fx"]=[{"fx":"fx-shake","strength":0.5}]
    clips.append(c); t+=L
  json.dump(proj(clips,media,True),open(a.out,'w',encoding='utf-8'),ensure_ascii=False); print("fast",N,"张",round(t,2),"秒"); sys.exit()
E=round(a.each-1/30,4)  # 结尾关键帧放在倒数一帧（30fps），不然最后一帧刚好回到 1 会顿一下
def clip(i,mid,L=a.each,end=E,zoom=a.zoom,ease=True,fx=True,fxs=a.fxs):
  c={"id":f"c{i+1:02d}","mediaId":mid,"start":round(i*a.each,4),"length":L,"offset":0,"kf":kf(zoom,end,ease)}
  if fx: c["fx"]=[{"fx":a.fx,"strength":fxs}]
  return c
def final():
  cs=[clip(i,f"m{i+1:02d}") for i in range(N)]
  for c in cs[1:]: c["transIn"]={"tr":a.tr,"length":a.trlen}
  cs[0]["anim"]={"in":{"id":"in-fade","dur":a.fin}}; cs[-1]["anim"]={"out":{"id":"out-fade","dur":a.fout}}
  return proj(cs,media,True)
json.dump(final(),open(a.out,'w',encoding='utf-8'),ensure_ascii=False)
print("final",N,"张",round(N*a.each,2),"秒")
if a.steps:
  os.makedirs(a.steps,exist_ok=True); m1=media[:1]; S=[]
  def one(**k): return proj([clip(0,"m01",**k)],m1)
  S.append(proj([],[]))                                                      # p01 空工程
  c=one(L=3,fx=False); del c["tracks"][0]["clips"][0]["kf"]; S.append(c)     # p02 第一张上主轨 3 秒
  c=one(L=3,fx=False); c["tracks"][0]["clips"][0]["kf"]={"sx":[{"t":3,"v":1}],"sy":[{"t":3,"v":1}]}; S.append(c)  # p03 结尾关键帧 1
  S.append(one(L=3,end=3,zoom=1.3,ease=False,fx=False))                      # p04 开头关键帧 1.3
  S.append(one(L=a.each,end=E,zoom=1.3,ease=False,fx=False))                 # p05 时长改 1 秒、结尾帧移到 0.97
  S.append(one(ease=False,fx=False))                                         # p06 开头改 1.08
  S.append(one(fx=False))                                                    # p07 缓出
  S.append(one(fxs=0.3))                                                     # p08 加柔光
  S.append(one())                                                            # p09 强度拉满
  S.append(proj([clip(i,"m01") for i in range(N)],m1))                       # p10 复制 N 份首尾相接
  S.append(proj([clip(i,f"m{i+1:02d}") for i in range(N)],media))           # p11 导入其余照片、换素材
  c=proj([clip(i,f"m{i+1:02d}") for i in range(N)],media)
  for x in c["tracks"][0]["clips"][1:]: x["transIn"]={"tr":a.tr,"length":a.trlen}
  S.append(c)                                                                # p12 接缝挂闪白叠化
  S.append(final())                                                          # p13 渐显渐隐
  for k,s in enumerate(S,1): json.dump(s,open(f"{a.steps}/p{k:02d}.json",'w',encoding='utf-8'),ensure_ascii=False)
  print("steps",len(S),"份 →",a.steps)
