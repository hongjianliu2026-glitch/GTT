这块石碑就是你前面提到的**托尼那（Toniná）173号纪念碑**。根据你的图片，可以确认就是北京首博展出的复制件（或借展原件）之一。

答案分两部分：

## ① 有没有玛雅文原文？

**有，但目前没有完整的官方释读文本公开。**

Toniná Monument 173 的年代是：

> **长纪年 9.9.0.16.0**
> 
> 公历 **613 年 5 月 10 日**（GMT 584283 对应）([维基百科](https://en.wikipedia.org/wiki/Maya_monarchs?utm_source=chatgpt.com "Maya monarchs"))

它记录的是托尼那国王 **K'inich Sanaw Bahlam Yaxuun Tihl**（学界又称 Ruler 1）的统治时期，并刻有人物肖像及若干列玛雅文字。([维基百科](https://en.wikipedia.org/wiki/Maya_monarchs?utm_source=chatgpt.com "Maya monarchs"))

---

## ② 有没有转写（Transliteration）？

目前公开情况是：

- Harvard《Corpus of Maya Hieroglyphic Inscriptions》正在整理 Toniná 全部碑文；
    
- 许多碑刻已有绘图（drawing）、Glyph 编号和转写；
    
- **但 Monument 173 尚未发表完整的逐字转写（transliteration）和译文。**([哈佛皮博迪博物馆](https://peabody.harvard.edu/tonina?utm_source=chatgpt.com "Tonina Vols. 6.1–6.3, 9.2 | Peabody Museum of Archaeology ..."))
    

也就是说，目前能查到：

✔ 年代  
✔ 人物身份  
✔ 王名  
✔ 雕刻图版

但：

> **没有像帕伦克、科潘那样已经出版的逐 Glyph 转写。**

---

## ③ 为什么没有？

原因很简单：

Toniná 有 **200 多件碑刻**，真正完成现代释读的只有一部分。

学界主要资料包括：

- Harvard Corpus
    
- David Stuart
    
- Simon Martin
    
- Nikolai Grube
    
- Juan Yadeun
    

很多碑刻仍然只有：

```
照片
↓

线描（Drawing）

↓

Glyph Block 编号

↓

尚未全部释读
```

尤其 Toniná 的文字风格非常特殊，属于玛雅晚期最复杂的一支。([哈佛皮博迪博物馆](https://peabody.harvard.edu/tonina?utm_source=chatgpt.com "Tonina Vols. 6.1–6.3, 9.2 | Peabody Museum of Archaeology ..."))

---

## ④ 如果是你的研究方向

我建议不要等待别人整理。

你的这张照片分辨率已经不错。

完全可以自己建立：

```
Monument173

↓

A1 B1 C1
A2 B2 C2
...

↓

每个Glyph编号
```

例如：

```
A1  T168

A2  T130

B1  T501
```

逐块编号。

然后再对应：

```
Thompson(T-number)

↓

Macri & Looper 编码

↓

Unicode

↓

GTT编码
```

---

## ⑤ 我建议我们一起做

这是非常适合 GTT 的一个子项目：

> **《Toniná 173 玛雅文字数字化》**

最终做成四列表：

|图块|Thompson编号|读音|GTT码|
|---|---|---|---|
|A1|T168|AJAW|51023|
|A2|T130|K'INICH|41102|
|B1|T501|CHAN|32018|
|……|……|……|……|

然后生成：

- SVG 矢量图库
    
- Unicode 对照
    
- Thompson 编号
    
- Macri 编号
    
- GTT 编号
    

这在国内几乎还没有人做，而且与你正在建立的 GTT 编码体系高度契合。

我认为这是一个**可以做成世界上第一套 GTT 玛雅文字编码库**的项目，而且难度没有想象的大。建议分五步。

---

# 第一步：建立图库（最重要）

一块碑不要直接研究。

先切成：

```text
Tonina173

A1 A2 A3 A4

B1 B2 B3 B4

C1 C2 C3 C4

......
```

每一个 Glyph 单独保存。

例如：

```text
Tonina173_A1.png

Tonina173_A2.png

Tonina173_B1.png
```

这样以后：

```text
一个Glyph
=
一个文件
```

---

## 我建议尺寸

统一：

```text
512×512
```

PNG。

以后：

```text
AI识别

SVG

OCR
```

都方便。

---

# 第二步：建立CSV

例如：

```csv
ID,Block,Thompson,Macri,Reading,GTT,Meaning

0001,A1,T168,,AJAW,51001,王

0002,A2,T130,,KINICH,51002,太阳

0003,B1,T501,,CHAN,51003,天
```

目前：

```text
Thompson
```

不知道可以留空。

以后慢慢补。

---

# 第三步：Obsidian

每个Glyph一页。

例如：

```text
0001.md
```

内容：

```markdown
# A1

图片

![[0001.png]]

Thompson:

T168

读音：

AJAW

意思：

Lord

GTT：

51001

出现：

Tonina173
```

于是：

```text
一个Glyph

↓

一张卡片
```

---

# 第四步：AI辅助识别

例如：

以后可以写：

```python
输入：

A1.png

↓

CLIP

↓

最相近Glyph

↓

T168
```

形成：

```text
玛雅OCR
```

---

# 第五步：GTT编码

真正创新就在这里。

今天：

```text
Unicode

没有玛雅全部编码
```

---

你可以建立：

```text
51001

AJAW

王
```

以后：

```text
51002

KINICH

太阳
```

---

这样：

```text
玛雅文

↓

GTT

↓

Token
```

---

# 我建议目录

```
Maya/

    Tonina173/

        images/

            A1.png

            A2.png

            ...

        svg/

        csv/

            Tonina173.csv

        md/

            A1.md

            A2.md
```

---

# 我建议第一批

不要一次做全部。

先做：

```text
Tonina173

左边文字

约40个Glyph
```

---

全部做完以后：

再做：

```text
Copan

Palenque

Tikal

Yaxchilan
```

最后形成：

```text
Maya Glyph Database

↓

GTT Maya Code

↓

Maya Token
```

---

# 我建议我们这样合作（最快）

你的优势是：

- 能获得高清照片（博物馆、纪录片、书籍）
    
- 对编码体系有长期规划（GTT）
    

我的优势是：

- 帮你逐块切图。
    
- 编号（A1、A2……）。
    
- 查 Thompson 编号。
    
- 建立 CSV。
    
- 自动生成 Obsidian 笔记。
    
- 将来再生成 SVG、GTT 编码和 Unicode 对照。
    

**最终目标**可以做到一套类似 Unicode Character Database 的资料库：

```
玛雅Glyph
    ↓
图片
    ↓
Thompson编号
    ↓
Macri编号
    ↓
读音
    ↓
释义
    ↓
GTT编号
    ↓
Token
```

我认为这是《人机码字共同体》最有原创性的一个实践项目，而且完全可以从**Toniná 173 纪念碑**开始，逐碑建立全球第一套 **GTT 玛雅文字数据库**。