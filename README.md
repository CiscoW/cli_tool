# cli_tool
自动生成代码工具CLI工具
## 使用方法
```python
python cli.py -cf config.yml
```
## 配置文件
```yml
# 全局变量配置
globals:
  # 模板输出位置 默认当前
  template_output: "./test"

  # 变量复用
  a: &A "RealValue"

# 代码工程结构定义
# folder_xx 代表xx文件夹
# file_xx 代表xx文件
# file_nil 代表只要创建文件夹不创建文件
# template_file 模板文件，默认为templates目录下同名xx文件，也可以指定
# substitute 指定模板文件中要替换的变量值
# 层级代表结构
folder_application:          # application文件夹
  file_demo.py:              # demo.py文件
    template_file:           # 默认为templates目录下同file_xx尾部xx同名文件，也可以指定
    substitute:              # 模板文件中要替换的变量
      ClassName: *A          # 可以采用引用全局变量

folder_notfile:
  file_nil: # nil 代表只要创建文件夹

```

## 模板文件
```python
class $ClassName(object):  # $xx代表xx为变量，可以通过在配置文件中设置实际值来替换
    pass
```
