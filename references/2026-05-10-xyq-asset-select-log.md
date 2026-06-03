# 2026-05-10 网页布局操作记录：从资产库选择

- 页面: `https://xyq.jianying.com/home?tab_name=home`
- 页面ID: `6F1A89EC31D145D87AD9753CF116F027`
- 步骤:
  1. 点击底部左侧 `上传参考素材` 按钮（约 `463,735`）。
  2. 在弹层里定位 `div`/`button` class `uploadMenuItem-GDs2iL`。
  3. 选择文本为 `从资产库选择` 的按钮。
  4. 成功后弹层保留，页面显示资产选择区域（含 `图片`/`视频` 标签与 `取消` 按钮）。
- 证据截图: `references/screenshots/2026-05-10-plus-from-asset-select.png`
- 结论: 当前布局可直接通过 DOM 文本点击，不依赖 `@`。
