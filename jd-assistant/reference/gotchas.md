# Gotchas

## 1. DocuSign login state

✗ **Bad:** Claude navigates to `https://app.docusign.com` and immediately tries
to upload the offer letter without checking whether the user is logged in.

✓ **Good:** Immediately after navigating to DocuSign, check for a login screen.
If a login prompt appears, pause and ask the user to log in, then wait for
confirmation before continuing.

**Why it matters:** DocuSign redirects unauthenticated sessions silently. If the
login check is skipped, the automation tries to click UI elements that don't exist
and fails mid-flow with no clear error.

---

## 2. Missing candidate details before entering the browser

✗ **Bad:** Claude reaches Phase 6, opens DocuSign in Chrome, and then asks mid-flow:
"What's the candidate's email address?"

✓ **Good:** If the user chose DocuSign delivery in Phase 1, collect the candidate's
full name and email address before Phase 6 begins — either in Phase 1 or at the
end of Phase 5. Never enter the browser flow without both fields.

**Why it matters:** Interrupting an open browser session to collect missing data
disrupts the automation state and confuses the user.

---

## 3. Re-asking for context the user already provided

✗ **Bad:** The user says "we need to hire a senior PM, fully remote, $160–180k"
and Phase 1 asks for role title, location, and compensation anyway.

✓ **Good:** Extract role title, location, and compensation from the message, confirm
them in a single sentence, and ask only for the fields that are genuinely missing.

**Why it matters:** The skill explicitly requires "one focused clarifying question
rather than a long form." Redundant questions break trust and slow the workflow.

---

## 4. Silently expanding the user's existing format

✗ **Bad:** The user has a 3-section job post on file. Claude produces a 7-section
post based on `references/job-post-structure.md` without asking.

✓ **Good:** Map the user's existing format against the reference, identify missing
sections, and ask one question: "Your existing JD has X and Y — want me to add Z,
or keep your current format?"

**Why it matters:** The user's format is the source of truth. Overriding it silently
may conflict with internal HR or legal standards the user hasn't mentioned.

---

## 5. Inventing compensation figures

✗ **Bad:** No salary range was provided, so Claude writes "$120,000–$150,000 DOE"
in the job post or offer letter.

✓ **Good:** If compensation isn't provided, omit the range from the job post entirely.
In the offer letter, use `[ANNUAL SALARY — confirm with HR]` as a bracketed placeholder.

**Why it matters:** Inventing compensation figures creates legal and HR liability.
The skill's instructions are explicit: "Don't invent a range."

---

## 6. 劳动法敏感词（中文JD场景）

✗ **Bad:** JD 中出现"30岁以下""限男性""已婚已育优先""限本地户籍"等表述。

✓ **Good:** 自动识别并替换敏感词——年龄→"年龄不限，需通过逻辑压力测试"，
性别→"性别不限，需具备岗位所需能力"，地域→"工作地点灵活，可远程协作"，
婚育→直接删除。

**Why it matters:** 中国《劳动法》《就业促进法》禁止就业歧视。JD 中出现
敏感词可能导致法律风险和企业声誉损失。

---

## 7. ATS 关键词遗漏

✗ **Bad:** 职责描述使用通用语言（如"负责数据分析"），没有行业可识别关键词。

✓ **Good:** 确保每项职责包含 2-3 个 ATS 系统识别词（如"用户画像建模""LTV/CAC分析"
"A/B测试""数据埋点"）。将通用职责转化为业务成果导向语言。

**Why it matters:** 大多数企业使用 ATS（Applicant Tracking System）筛选简历，
JD 中缺少 ATS 关键词会导致匹配率下降，优质候选人可能被系统过滤。

---

## 8. 首屏吸引力不足

✗ **Bad:** JD 开头是"我们正在招聘一位产品经理，负责产品规划工作"——平淡无奇。

✓ **Good:** 设计首屏黄金30字，用 FABE 法则突出核心价值——如"主导千万级DAU产品的
增长策略，12个月内将推荐转化率提升15%+，直接向VP汇报"。

**Why it matters:** 候选人浏览 JD 的平均时长不到30秒。首屏决定了是否继续阅读。

---

## 9. 模式路由误判

✗ **Bad:** 用户说"帮我写个JD顺便出点面试题"，技能判断为快速JD模式，只输出了JD文本。

✓ **Good:** 用户同时提到 JD 和面试题，属于完整招聘包需求，应路由到完整模式。
判断原则：只要涉及 JD 以外的招聘文档（面试指南、Offer Letter），就走完整模式。

**Why it matters:** 模式误判导致用户需要二次发起请求，体验割裂。
