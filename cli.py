"""
自动生成项目代码CLI工具
"""
import os
import yaml
import click
from string import Template
from typing import (AnyStr, Dict)


class Cli(object):
    def __init__(self, config_file: str):
        if not os.path.exists(config_file):
            raise Exception(f"{config_file}配置文件不存在！")

        self.config = self.load_config(self.read_file(config_file))
        self.project = []

    @staticmethod
    def read_file(file: str) -> AnyStr:
        """
        读取文件中的数据
        :param file:
        :return:
        """
        with open(file, "r", encoding="utf-8") as f:
            data = f.read()
        return data

    @staticmethod
    def write_file(file: str, data: AnyStr):
        """
        向文件中写入数据
        :param file:
        :param data:
        :return:
        """
        with open(file, "w+", encoding="utf-8") as f:
            f.write(data)

    @staticmethod
    def load_config(data: AnyStr) -> Dict:
        """
        转换yaml数据为字典
        :param data:
        :return:
        """
        return yaml.load(data, Loader=yaml.FullLoader)

    @staticmethod
    def mkdir(path: str):
        """
        创建文件夹，如果已经给存在就不需要创建
        :param path:
        :return:
        """
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def parsing_folder_and_file(template_output: str, folder_or_file: str) -> (str, str):
        """
        判断是文件还是文件夹
        :param template_output:
        :param folder_or_file:
        :return: 返回文件或文件夹路径
        """
        file_name = ""
        folder_head = "folder_"
        file_head = "file_"
        if folder_or_file.startswith(folder_head):
            return os.path.join(template_output, folder_or_file[len(folder_head):]), file_name

        elif folder_or_file.startswith(file_head):
            file_name = folder_or_file[len(file_head):]
            return template_output, file_name
        else:
            raise Exception(f"{folder_or_file}命名不符合规范")

    @staticmethod
    def substitute(template_data: AnyStr, kv: Dict) -> AnyStr:
        """
        替换模板中的变量
        :param template_data:
        :param kv:
        :return:
        """
        s = Template(template_data)
        return s.substitute(kv)

    def recursive_config_data(self, config: dict, template_output: str):
        """
        递归调用获取全部要生成的文件
        :param config:
        :param template_output:
        :return:
        """
        for k, v in config.items():
            template_output, file_name = self.parsing_folder_and_file(template_output, k)
            if file_name:
                self.project.append(
                    {
                        "file_name": file_name,
                        "path": template_output,
                        "config": v,

                    }
                )
            else:
                self.recursive_config_data(v, template_output)

    def create_folder_file(self, obj: dict):
        """
        创建文件夹及其包含的文件
        :return:
        """
        file_name = obj.get("file_name")
        path = obj.get("path")
        config = obj.get("config")
        file_path = os.path.join(path, file_name)
        # 创建文件夹
        self.mkdir(path)
        if file_name != "nil":
            # 如果不等于nil则需要创建文件
            template_file = config.get("template_file")

            if not template_file:
                # 没有配置模板文件位置默认在templates下找同名文件
                template_file = os.path.join("templates", file_name)
            else:
                template_file = os.path.join("templates", template_file)

            if os.path.exists(template_file):
                self.mkdir(path)
                data = self.read_file(template_file)
                substitute = config.get("substitute")
                # 替换文件内容中的变量
                if substitute:
                    self.write_file(file_path, self.substitute(data, substitute))
                else:
                    # 不需要替换变量文件
                    self.write_file(file_path, data)
            else:
                # 创建空文件
                self.write_file(file_path, "")
                click.echo(f"模板文件未找到{template_file}，将创建空文件")
            click.echo(f"auto create: {file_path}")

    def auto_create_project(self):
        """
        自动创建代码工程
        :return:
        """
        template_output = self.config.get("globals", {}).get("template_output", "")
        del self.config["globals"]
        self.recursive_config_data(self.config, template_output)
        for obj in self.project:
            self.create_folder_file(obj)


@click.command()
@click.option("-cf", default="config.yml", help="配置文件")
def main(cf: str):
    """CLI工具"""
    try:
        cli = Cli(cf)
        cli.auto_create_project()
    except Exception as e:
        click.echo(e)


if __name__ == '__main__':
    main()
