
第六章 Tokenizer：机器的新文字

传统计算机直接处理字符。

大语言模型并不如此。

模型首先使用Tokenizer把文本切分成Token。

例如：

internationalization

→ inter
→ national
→ ization

对于中文：

中华人民共和国

→ 中华
→ 人民
→ 共和国

Token成为机器真正认识的“字”。

人类看到字符，模型看到Token。