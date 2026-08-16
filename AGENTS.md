<!-- hoshivel:agent-rules v1 -> https://github.com/Hoshivel/workspace -->

# AGENTS.md — hoshi-standards（公開）

> **代理執行規範的正本不在這裡**，在
> [workspace](https://github.com/Hoshivel/workspace) 的 `AGENTS.md`：
> 四層記錄（焦點／todo／logs／decisions）、中斷復原流程、跨倉庫協作流程、
> 分支與 PR 規則全在那裡。
> 本檔只補上**這個倉庫自己的**東西。
>
> **本倉庫是公開的。** 外部讀者不需要 workspace——讀 `README.md` 與那兩份
> 規範就夠了。§0 是給 Hoshivel 自己的代理看的。

## 0. 開工前

**先取得 workspace，讀它的 `focus.md` 與 `AGENTS.md`。**

```sh
cat ../workspace/focus.md                                          # 本機：就在旁邊
git clone https://github.com/Hoshivel/workspace.git ../workspace   # 雲端：自己補上
```

- 取不到就**停下來告訴使用者**，不要退回在本倉庫自建 `TODO.md` 或工作記錄。
- **本倉庫的待辦在 `workspace/todo/hoshi-standards/`**，工作日誌在 `workspace/logs/hoshi-standards/`。
  **不得**自建 `TODO.md`／`logs/`，也不得記錄領取、分支或 `Status: Editing`
  （workspace `AGENTS.md` §4.4、§5）。
- 續接既有任務時**沿用該事項記的分支與 PR**，不要另開新分支
  （workspace `AGENTS.md` §4.3）。

## 1. 入場閱讀順序

1. `README.md` —— 本倉庫的定位，以及**什麼會進這裡**。
2. `conventions/api.md` —— 協定慣例。新增任何端點或欄位前必讀。
3. `protocols/versioning.md` —— 升版與破壞性變更的判準。

## 2. 驗證

本倉庫只有 Markdown，沒有建置步驟。改動後執行：

```sh
python3 tools/check-links.py     # 相對連結指不到東西就是紅燈
```

**這一項不要用眼睛對。** 一條壞掉的相對連結在 GitHub 上是安靜的 404，
diff 上看不出來——腳本就是為此存在的，`ci.yml` 也跑同一支。
先在本機跑過再推（workspace `AGENTS.md` §1.7.3：CI 不是第一道驗證）。

其餘兩項腳本看不到，靠審閱守住：

- 規範關鍵字（必須／不得／應／不宜／可）用得符合 `conventions/api.md` §0.2。
- 條文與理由分開：要求寫在正文，理由寫在 `> **註**` 區塊。

## 3. 這個倉庫的特殊規則

- **這是公開倉庫。不得放進任何內部的東西。** 判準是 workspace `AGENTS.md`
  §1.10.1 那一句：**這段文字讓讀者更容易攻擊我們嗎？** 具體不得出現——
  內部架構與服務拓撲、資料流與信任邊界、金鑰與簽章的組成方式、主機名稱與
  內網位址、埠與路徑的對應、部署結構、指向私有倉庫內容的路徑。
  **倉庫名稱與連結本身可以。**
- **一條規則要進來，得先通過「換到別人的系統還成立嗎」。** 只對某一套服務
  拓撲成立的規則不屬於這裡——那種規則寫進公開倉庫，對外面的人沒有用，
  而且它描述的正是我們的拓撲。
- **舉例要用中性的名字**（`billing`、`user-directory`），不得用自家服務名。
  一份規範的舉例會被逐字抄走，那是它最容易洩漏內部命名的地方。
- **不得開始收實作。** 可被 import 的東西一律屬於
  [hoshi-sdk](https://github.com/Hoshivel/hoshi-sdk)。
- 規範關鍵字依 RFC 2119 使用，理由寫進 `> **註**` 區塊。術語依
  `conventions/api.md` §0：用**標準協定**，不用「契約」。
- 文件沿用既有風格：**正體中文為主**，程式碼註解英文。
