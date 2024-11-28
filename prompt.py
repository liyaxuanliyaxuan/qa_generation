navie_prompt = """"Based on the following content, generate at least 10 question-answer pairs. Return the result as a JSON array where each object has the format {{\"instruction\": question, \"input\": \"\", \"output\": answer}}"""

nice_prompt = """ 请从给定的 Markdown 格式的物理书籍中提取问题，并根据问题推导出解答。书籍内容应包含以下关键信息：\n- 问题描述\n- 背景信息\n- 已知量和未知量\n- 使用的物理定律和公式\n\n**如果书籍中缺少某些关键信息**，请在输出中进行补充。\n\n在解答过程中，**请注意以下操作类型（operation）的取值**：\n1. **代入已知量**：将已知的数值代入公式或方程。\n2. **公式变形**：对公式进行代数变换或重新排列。\n3. **计算**：进行数值计算以得到中间结果。\n4. **假设**：对未知量或未给出的条件做出合理假设。\n5. **单位转换**：进行单位的转换，确保单位一致。\n6. **逻辑推理**：根据物理定律与已知条件进行推理。\n7. **最终计算**：将所有中间结果代入最终公式得到最终答案。\n\n生成的解答应包括每个步骤的推理过程，确保每个步骤的推理清晰且符合物理规律。公式请使用 LaTeX 格式。\n\n请按照以下输出格式生成解答：\n\n### 输出格式：\n\n{ \n  \"question\": \"{{question}}\", \n  \"context\": \"{{context}}\", \n  \"known_variables\": {{known_variables}}, \n  \"unknown_variables\": {{unknown_variables}}, \n  \"laws_and_equations\": {{laws_and_equations}}, \n  \"reasoning_steps\": [ \n    { \n      \"operation\": \"代入已知量\", \n      \"result\": \"计算结果或中间结果\", \n      \"explanation\": \"解释该步骤的物理意义，公式使用 LaTeX 格式\" \n    }, \n    { \n      \"operation\": \"公式变形\", \n      \"result\": \"计算结果或推导出的中间结果\", \n      \"explanation\": \"公式变形，得出未知量，使用 LaTeX 格式\" \n    }, \n    { \n      \"operation\": \"计算\", \n      \"result\": \"计算结果\", \n      \"explanation\": \"进行数值计算并给出物理背景\" \n    },  \n    { \n      \"operation\": \"最终计算\", \n      \"result\": \"最终计算结果\", \n      \"explanation\": \"汇总中间结果并完成最终计算\" \n    } \n  ], \n  \"continuous_reasoning\": \"在本题中，我们代入已知量，进行公式变形和计算，通过假设简化问题，并确保单位一致，最后通过逻辑推理得到答案。\",  \n  \"units_check\": \"检查最终答案的单位是否合理\", \n  \"final_answer\": \"推导出的最终答案，附带单位（如 v = 10 m/s）\" \n} """
  
one_shot_prompt = '''
    我给出一些文字，其中包含物理领域的题目。请你将所有的题目以json的格式提取出来，要求如下：
    1. 每个题目包含“question”，“real_answer”两个字段；
    2. 'question'中包含问题，‘real_answer’ 中包含答案；
    3. 'question'和'real_answer'中涉及到公式的部分必须使用Latex格式给出；
    4. 输出中必须只包含json内容，不能包含其他任何内容；
    5. 仅输出10个问答对。
    比如：
    [{"question": "函数  f(u, v)  由关系式  f[x g(y), y]=x+g(y)  确定, 其中函数  g(y)  可微, 且  g(y) \\neq 0 , 则  \\frac{\\partial^{2} f}{\\partial u \\partial v}= \n", "real_answer": "【答案】设  u=x g(y), v=y , 不难得出  x=\\frac{u}{g(v)}, y=v , \n\n代入即得  f(u, v)=\\frac{u}{g(v)}+g(v) . \n\n\n 于是\n\n\\frac{\\partial f}{\\partial u}=\\frac{1}{g(v)}, \\quad 
    \\frac{\\partial^{2} f}{\\partial u \\partial v}=-\\frac{g^{\\prime}(v)}{[g(v)]^{2}} .\n\n\n综上可知，可以得到上面的答案。"},
    {"question":"电荷量分别为 q1 和 q2 的两个静止的点电荷，相距为 r，试求下列情况下它们之间的相互作用力，即 q1 作用在 q2 上的力 F21 和 q2 作用在 q1 上的力 F12：(1) q1 和 q2 都在真空中；(2) q1 和 q2 都在均匀介质中；(3) q2 在导体壳腔内，但 q1 在导体外。","real_answer":"在上述三种情况下，q1 作用在 q2 上的力都是 F_{21} = \\frac{1}{4\\pi\\epsilon_0} \\frac{q1 q2}{r^2} \\mathbf{e_{12}}，式中 \\mathbf{e_{12}} 是从 q1 到 q2 方向上的单位矢量。q2 作用在 q1 上的力都是 F_{12} = -F_{21} = -\\frac{1}{4\\pi\\epsilon_0} \\frac{q1 q2}{r^2} \\mathbf{e_{12}}。"}]
    '''

cot_prompt = '''
    我给出包含物理领域的题目和正确答案。请你根据问题和答案进行逐步骤的推理：
    输入要求：
    1. 每个题目包含“question”，“real_answer”两个字段；
    2. 'question'中包含问题，‘real_answer’ 中包含答案；
    输出要求：
    1. 'question'和'answer'中涉及到公式的部分必须使用Latex格式给出；
    2. 输出中必须只包含json内容，不能包含其他任何内容；
    3. 'question'为原问题，’answer‘为包含正确推理步骤的回答。
'''

one_shot_prompt_formatted='''
    我给出一些文字，其中包含物理领域的题目。请你将所有的题目以json的格式提取出来，要求如下：
    1. 每个题目包含“question”，“real_answer”两个字段；
    2. 'question'中包含问题，‘real_answer’ 中包含答案；
    3. 'question'和'real_answer'中涉及到公式的部分必须使用Latex格式给出；
    4. 输出中必须只包含json内容，不能包含其他任何内容；
    5. 仅输出10个问答对。
    比如：
    ```json
    [{"question": "函数  f(u, v)  由关系式  f[x g(y), y]=x+g(y)  确定, 其中函数  g(y)  可微, 且  g(y) \\neq 0 , 则  \\frac{\\partial^{2} f}{\\partial u \\partial v}= \n", "real_answer": "【答案】设  u=x g(y), v=y , 不难得出  x=\\frac{u}{g(v)}, y=v , \n\n代入即得  f(u, v)=\\frac{u}{g(v)}+g(v) . \n\n\n 于是\n\n\\frac{\\partial f}{\\partial u}=\\frac{1}{g(v)}, \\quad 
    \\frac{\\partial^{2} f}{\\partial u \\partial v}=-\\frac{g^{\\prime}(v)}{[g(v)]^{2}} .\n\n\n综上可知，可以得到上面的答案。"},
    {"question":"电荷量分别为 q1 和 q2 的两个静止的点电荷，相距为 r，试求下列情况下它们之间的相互作用力，即 q1 作用在 q2 上的力 F21 和 q2 作用在 q1 上的力 F12：(1) q1 和 q2 都在真空中；(2) q1 和 q2 都在均匀介质中；(3) q2 在导体壳腔内，但 q1 在导体外。","real_answer":"在上述三种情况下，q1 作用在 q2 上的力都是 F_{21} = \\frac{1}{4\\pi\\epsilon_0} \\frac{q1 q2}{r^2} \\mathbf{e_{12}}，式中 \\mathbf{e_{12}} 是从 q1 到 q2 方向上的单位矢量。q2 作用在 q1 上的力都是 F_{12} = -F_{21} = -\\frac{1}{4\\pi\\epsilon_0} \\frac{q1 q2}{r^2} \\mathbf{e_{12}}。"}]
    ```
    '''


complete_prompt='''
我给出一道物理问题和它的正确答案，请你将题目改为包含4个选项的选择题，要求如下：
1. 4个选项中包含一个正确答案，和三个错误答案；
2. 问题来自我给出的<question><question>标记中的内容；正确答案参考我给出的<answer><answer>标记中的内容，错误答案根据正确答案进行改编，但要和题目相关；
3. 4个选项分别放入 choice1、choice2、choice3、choice4 字段；问题放入question；answer字段为答案的标号，可能的值为 A/B/C/D。 A/B/C/D标号分别对应choice1/choice2/choice3/choice4；
4. 返回的内容以格式化json给出。

比如：
{
        "question": "一个做匀速直线运动的物体，突然受到一个与运动方向不在同一直线上的恒力作用时，那么物体的运动为",
        "choice1": "一定做曲线运动",
        "choice2": "可能做直线运动，也可能做曲线运动",
        "choice3": "继续做直线运动",
        "choice4": "运动的形式不能确定",
        "answer": "A"
}
'''