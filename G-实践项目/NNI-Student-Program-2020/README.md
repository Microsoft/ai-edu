# 基于自动机器学习工具 NNI 的创新性科研扩展项目 
## 1. 项目介绍
本项目以开源自动机器学习工具 NNI 为基础，立足 NNI 的丰富工具用例与可扩展性，希望能够帮助同学们加强对机器学习的了解与认识，服务于同学们的科研项目与实践，在帮助同学们取得优秀科研成果的同时，进一步提高 NNI 的实用性和丰富性。​

项目导师：Scarlett Li、Tingting Qin、Hui Xue、Quanlu Zhang

<br>

## 2. 必备技能
### A. 学习 Git/Github 基本操作
本项目要求同学们创建自己的 Git 仓库，通过 Git / Github 托管自己的代码和文档，并在 ai-edu 的 Issue 里提交你的 repo 地址。因此，同学们需掌握基本的 Git / Github 操作。

### B. 使用 Markdown 编写文档
每个任务要求提交一份使用 Markdown 编写的文档，其中包括环境配置、必要的代码和说明、实验结果及分析等。因此，同学们需掌握必要的 Markdown 语法。正如你所见，此文档就是使用 Markdown 编写。

### C. Python与机器学习/深度学习基础
本项目的样例代码绝大多数使用 Python 作为编程语言编写，因此需要同学们掌握一定的 Python 基础。此外，为了理解示例代码并完成任务，还需要有一定的机器学习/深度学习基础。

<br>

## 3. 任务列表

我们为同学们设置了四个不同难度的任务来帮助大家探索自己的进阶之路：

1. [Task1 入门任务](./Task-Release/Task1/README.md)

2. [Task2 进阶任务 HPO+NAS](./Task-Release/Task2/README.md)

3. [Task3 进阶任务 Feature Engineering](./Task-Release/Task3/README.md)

4. [Task4 自主任务](./Task-Release/Task4/README.md)

<br>

## 4. 时间安排

+ 第一轮 DDL：2021.2.7
  + Task 1、Task 2.1、Task 3.1、Task 4 启动报告
+ 第二轮 DDL：2021.3.14
  + Task 2.2、Task 3.2、Task 4 中期报告（不强制）
+ 第三轮 DDL：2021.4.4
  + Task 4 结项报告

<br>

## 5. 提交方式

1. 每个队伍需要在 [Github](https://github.com/) 中创建自己的 public repo，并按照 [Team-Submission](./Team-Submission) 中的参考格式管理自己的文档和代码。
2. 每个队伍在完成某个任务后，首先 commit 本地的修改，并通过 `git push` 上传至自己的 repo ，之后再向 [本Issue](https://github.com/microsoft/ai-edu/issues/582) 提交相关信息（可编辑提交信息来更改任务完成情况），格式如下：

```
1. 团队名：
2. 团队人员：
3. 团队学校：
4. 任务完成情况：
5. Github Repo地址：
6. 补充信息（若有）：比如，您可以在这部分简要说明您对 NNI 的 contribution
```

我们会选择优秀的项目合并到官方 repo 中。

注：在您提交时，需要按照下面的形式组织文件。 

```
.
├── Task1
│   ├── README.md
│   └── code     # a folder
├── Task2
│   ├── README.md
│   └── code     # a folder
├── Task3
│   ├── README.md
│   └── code     # a folder
├── Task4
│   ├── README.md
│   └── code     # a folder
└── README.md    
```

<br>

## 6. 项目答疑

如果您在实验过程中遇到一些问题，您可以先在官方微信群里与其他的小伙伴们交流，或者阅读 [NNI官方文档](https://nni.readthedocs.io/en/latest/index.html) 与 [NNI FAQ](https://nni.readthedocs.io/en/latest/Tutorial/FAQ.html)。

如果您的问题还是没有得到解决，请到 NNI官方 [Github issues](https://github.com/microsoft/nni/issues/new/choose) 中选择“Question for NNI Student Program China / NNI 学生项目问题表单”提出您的问题。

<br>

## 7. 参考资料

[NNI 官方文档](https://nni.readthedocs.io/en/latest/index.html)与[Github 仓库](https://github.com/microsoft/nni)

[Git 中文文档](https://git-scm.com/book/zh/v2)与[GitHub 帮助文档](https://docs.github.com/cn/github)

[Markdown 中文文档](https://markdown-zh.readthedocs.io/en/latest/)

[Python 中文文档](https://docs.python.org/zh-cn/3/)，[PyTorch 官方文档](https://pytorch.org/docs/stable/index.html)以及[Tensorflow API 文档](https://tensorflow.google.cn/api_docs/python/tf)

<br>

**关于[微软人工智能教育与学习共建社区](https://github.com/microsoft/ai-edu)**

本社区是微软亚洲研究院（Microsoft Research Asia，简称MSRA）人工智能教育团队创立的人工智能教育与学习共建社区。

在教育部指导下，依托于新一代人工智能开放科研教育平台，微软亚洲研究院研发团队和学术合作部将为本社区提供全面支持。我们将在此提供人工智能应用开发的真实案例，以及配套的教程、工具等学习资源，人工智能领域的一线教师及学习者也将分享他们的资源与经验。

正如微软的使命“予力全球每一人、每一组织，成就不凡”所指出的，期待借由本社区的建立，能以开源的方式，与广大师生、开发者一起学习、一起贡献，共同丰富、完善本社区，既而为中国人工智能的发展添砖加瓦。
