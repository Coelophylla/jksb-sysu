# jksb-sysu

本项目实现了针对中山大学学生健康状况申报要求的每日定时申报，并可通过email自动发送申报结果。本项目通过Github Actions定期执行，无需开启电脑或租用服务器。

**受网络状况和Github服务器的影响，申报结果存在不确定性，请谨慎使用**

## 任务流程

1. 登录中山大学中央身份验证服务
2. 沿用上一次提交的填报内容
3. 提交申报


## 技术方案

- python+selenium+firefox+ddddocr
- 通过Github Action定期执行自动申报代码

## 项目配置

### 0. 创建一个Github账号

自动申报的结果将通过email发送到注册该账号所用的邮箱。

### 1. 生成自己的仓库

点击右上角的Fork按钮，将代码fork到自己的仓库。

### 2. 填写账号密码

2.1 在fork出来的仓库中点击最右侧的Settings，然后在左侧竖栏中选择Secrets-Actions。

2.2 点击右上角的New repository secret按钮，在Name一栏填入`NETID`(*注意需要大写*),在Value一栏填入你的NetID，点击Add secret保存。

2.3 再次点击右上角的New repository secret按钮，在Name一栏填入`PASSWORD`(*注意需要大写*),在Value一栏填入你的密码，点击Add secret保存。

### 3. 定时运行

点击位于Settings同一栏的Actions，确认启用workflow后，选择名字为jksb的工作流，启用。

默认配置为，每天 23:32 UTC (*我们这里是UTC +8，相当于7：32 a.m.*)运行。

控制Github Action自动运行的文件是/.github/workflows/jksb.yml，如需修改定时运行时间，则修改该文件的`- cron:  '32 23 * * *'`一行，修改方法可参考[该文档](https://docs.github.com/en/actions/learn-github-actions/events-that-trigger-workflows#scheduled-events)。

### 4. 修改Github Actions的通知方式（可选）

Github的默认通知方式为：当Actions执行成功时不通知，执行失败时邮件通知。

如需每次运行时均进行通知，可按照以下步骤修改设置：

4.1 点击右上角自己的头像，选择Settings

4.2 在左侧竖栏中选择Notifications，下拉找到Actions一栏

4.3 取消勾选Send notifications for failed workflows only 

### 5. 手动测试（可选）

在自己仓库的Actions一栏中选择jksb工作流，点击右下角的Run workflow可手动运行，以测试能否正确填报。

如出错，可在该次运行结果的右侧`...`中选择View workflow file，再点击左侧的build以查看报错信息。

## 免责声明

使用本软件直接或间接造成的损失由使用者承担，请谨慎使用。

如遇身体不适，健康码颜色变化或居住地址发生变化等情况，请及时更新健康申报信息。

## 致谢

本项目的框架和流程参考[@Editi0](https://github.com/Editi0)的[jksb_sysu](https://github.com/Editi0/jksb_sysu)项目，该项目最早由 [@tomatoF](https://github.com/tomatoF) 开发。

## 项目维护

欢迎各位提交自己的修改。由于已离开中大，@Coelophylla难以继续对项目进行维护。希望有同学愿意参与/接手这个项目。有意者可创建issue自荐。