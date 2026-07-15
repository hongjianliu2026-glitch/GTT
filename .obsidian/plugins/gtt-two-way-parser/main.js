const { Plugin, Notice } = require("obsidian");

module.exports = class GTTTwoWayParser extends Plugin {
  async onload() {
    new Notice("GTT 双向码字插件已加载");

    this.k2j = {};
    this.j2k = {};

    try {
      const csv = await this.app.vault.adapter.read(
        ".obsidian/plugins/gtt-two-way-parser/dict.csv"
      );

      csv.split(/\r?\n/).forEach(line => {
        line = line.trim();
        if (!line) return;

        const parts = line.split(/[,\，]/);
        if (parts.length >= 2) {
          const code = parts[0].trim();
          const char = parts[1].trim();

          this.k2j[code] = char;
          this.j2k[char] = code;
        }
      });

      new Notice(
        "K2J/J2K 字典加载：" + Object.keys(this.k2j).length + " 条"
      );

    } catch (e) {
      new Notice("dict.csv 读取失败：" + e.message);
      console.error(e);
      return;
    }

    this.registerMarkdownPostProcessor((el) => {
      let html = el.innerHTML;

      // K2J：码到字
      html = html.replace(/K2J\{([^}]+)\}/g, (match, content) => {
        return content.replace(/\d+/g, code => {
          return this.k2j[code] || code;
        });
      });

      // J2K：字到码
      html = html.replace(/J2K\{([^}]+)\}/g, (match, content) => {
        let result = "";
        for (const ch of content) {
          result += this.j2k[ch] || ch;
        }
        return result;
      });

      el.innerHTML = html;
    });
  }
};