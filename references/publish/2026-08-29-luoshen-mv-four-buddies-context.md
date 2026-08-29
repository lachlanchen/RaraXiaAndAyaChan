# 《洛神》MV 发布审核上下文

## 作品身份

- 歌曲：乱徵《洛神》
- 文本源头：三国曹植《洛神赋》原文选段
- 画面：洛神舞者是主角；啦啦侠、阿芽酱、飒飒君和庄子机器人坐在舞台侧边，像真实演出观众一样轻轻挥动荧光棒。
- 气质：写实电影感古风，温柔、典雅、梦幻。

## ASR 与时间轴原则

1. 以视频实际音轨的 ASR 时间轴为唯一时间证据。
2. 下列原文用于修正歌唱 ASR 的同音错字，不得用整篇赋文替换真实音轨。
3. 只保留实际唱到的句子和重复；不添加未唱出的句子。
4. 普通文字校正必须保留 ASR 的 cue 数量、开始时间和结束时间。
5. 中文是此音轨的原语言；发声标记应跟随中文行。

## 已核对的实际唱段

原始 ASR 已定位到下列《洛神赋》选段。校正时逐 cue 使用，保持现有 15 个 cue 的时间轴；本片段没有“秾纤得衷”段，也没有结尾重复：

```text
1. 披罗衣之璀粲兮
2. 珥瑶碧之华琚
3. 戴金翠之首饰
4. 缀明珠以耀躯
5. 践远游之文履
6. 曳雾绡之轻裾
7. 芳泽无加
8. 铅华弗御
9. 翩若惊鸿
10. 婉若游龙
11. 荣曜秋菊
12. 华茂春松
13. 髣髴兮
14. 若轻云之蔽月
15. 飘飖兮若流风之回雪
```

## 审核译文

译文应根据 ASR cue 逐句取用；如一个 cue 只唱半句，译文也保留对应半句。

### English

```text
She wears robes of radiant splendor.
Splendid jade earrings adorn her.
Gold and kingfisher ornaments crown her hair.
Bright pearls are strung to illuminate her form.
She steps in patterned shoes made for distant wandering.
A light, mistlike hem trails behind her.
No added fragrance perfumes her.
No powder colors her face.
Light as a startled swan goose.
Graceful as a roaming dragon.
Radiant as chrysanthemums in autumn.
Flourishing as pines in spring.
She seems,
like a light cloud veiling the moon,
like a drifting breeze that whirls the returning snow.
```

### 日本语

```text
燦然と輝く羅衣をまとい、
美しい瑶碧の耳飾りをつける。
金と翡翠の髪飾りを戴き、
明珠を連ねてその身を輝かせる。
遠遊の文様ある履を踏み、
霧のように薄い裾を引く。
香りを加えず、
白粉も施さない。
驚く雁のように軽やかに、
遊ぶ龍のようにしなやかに。
秋菊のように輝き、
春の松のように栄える。
その姿は、
薄雲が月を覆うようであり、
流れる風が雪を舞い返すようである。
```

### Français

```text
Elle porte une robe d'une splendeur éclatante.
De magnifiques pendants de jade l'ornent.
Des parures d'or et de plumes de martin-pêcheur couronnent ses cheveux.
Des perles lumineuses font rayonner sa silhouette.
Elle avance dans des souliers brodés faits pour les lointains voyages.
Un léger ourlet, pareil à la brume, traîne derrière elle.
Aucun parfum ajouté ne l'embaume.
Aucun fard ne colore son visage.
Légère comme une oie sauvage surprise.
Gracieuse comme un dragon qui serpente.
Rayonnante comme les chrysanthèmes d'automne.
Florissante comme les pins au printemps.
Elle semble,
tel un léger nuage voilant la lune,
tel un souffle errant qui fait tournoyer la neige.
```

## 元数据上下文

元数据应简洁、面向观众，不要把分镜或整段歌词当作描述。可表达的核心是：古典舞蹈与曹植《洛神赋》相遇，洛神在花海、云海和古建筑之间起舞，四位伙伴在舞台侧边安静观演。标题与描述应正确标出歌曲为乱徵《洛神》，文本源自曹植《洛神赋》。发布分类为 `lalamv`。
