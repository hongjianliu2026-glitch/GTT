const { Plugin, Notice } = require("obsidian");

module.exports = class GTTCodeParser extends Plugin {
  async onload() {
    new Notice("GTT Code Parser 已加载");

    this.dict = {};

    try {
      const csv = await this.app.vault.adapter.read(
        ".obsidian/plugins/gtt-code-parser/dict.csv"
      );

      csv.split(/\r?\n/).forEach(line => {
        line = line.trim();
        if (!line) return;

        const parts = line.split(/[,\，]/);
        if (parts.length >= 2) {
          const code = parts[0].trim();
          const value = parts[1].trim();
          this.dict[code] = value;
        }
      });

      new Notice("GTT 字典加载：" + Object.keys(this.dict).length + " 条");

    } catch (e) {
      new Notice("CSV读取失败：" + e.message);
      console.error(e);
      return;
    }

    this.registerMarkdownPostProcessor((el) => {
      const walker = document.createTreeWalker(
        el,
        NodeFilter.SHOW_TEXT,
        {
          acceptNode: (node) => {
            const parent = node.parentElement;
            if (!parent) return NodeFilter.FILTER_REJECT;

            if (
              parent.closest("code") ||
              parent.closest("pre") ||
              parent.closest("script") ||
              parent.closest("style")
            ) {
              return NodeFilter.FILTER_REJECT;
            }

            return NodeFilter.FILTER_ACCEPT;
          }
        }
      );

      const nodes = [];
      while (walker.nextNode()) {
        nodes.push(walker.currentNode);
      }

      for (const node of nodes) {
        node.nodeValue = node.nodeValue.replace(/\b\d+\b/g, (code) => {
          const n = parseInt(code, 10);

          // 限制1：小于10不替换
          if (n < 10) return code;

          // 限制2：不在字典里不替换
          if (!this.dict[code]) return code;

          return this.dict[code];
        });
      }
    });
  }
};