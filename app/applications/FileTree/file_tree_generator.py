import os


class FileTreeGenerator:
    """目录树生成器"""

    def __init__(self, root_path, **kwargs):
        """
        :param root_path: 根目录路径
        """
        self.__root_path: str = root_path
        self.__site: list = []
        self.__output: str = ""
        self.__generate_flag: bool = False
        self.__kwargs = kwargs
        self.__init_kwargs()

    def __init_kwargs(self):
        """
        初始化参数
        :return: None
        """
        #
        self.set_max_depth(self.__kwargs.get("max_depth", -1))
        #
        _ignore_names = self.__kwargs.get("ignore_names", [])
        self.__kwargs["ignore_names"] = []
        self.__kwargs["ignore_suffix"] = []
        self.add_ignore_names(_ignore_names)
        #
        _zip_suffix = self.__kwargs.get("zip_suffix", [])
        self.__kwargs["zip_suffix"] = []
        self.add_zip_suffix(_zip_suffix, self.__kwargs.get("zip_suffix_minimum", 0))

    def draw(self, save_path=None, cmd=True):
        """
        打印文件目录树状图
        :param save_path: 保存路径(默认为控制台)
        :param cmd: 是否在控制台显示
        :return: 目录树状图
        """
        if not self.__generate_flag:
            self.__generate_file_tree(self.__root_path, depth=0)
            self.__generate_flag = True
        if save_path:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(self.__output)
        if cmd:
            print(self.__output)
        return self.__output

    def reset(self, **kwargs):
        """
        重置
        :return: None
        """
        self.__site.clear()
        self.__output = ""
        self.__generate_flag = False
        self.__kwargs = kwargs
        self.__init_kwargs()

    def set_max_depth(self, max_depth: int):
        """
        设置最大深度
        :param max_depth: 最大深度
        :return: None
        """
        if self.__generate_flag:
            raise ValueError("max_depth cannot be set after drawing")
        if max_depth < 0 and max_depth != -1:
            raise ValueError("max_depth must be a positive integer or -1")
        self.__kwargs["max_depth"] = max_depth

    def add_ignore_names(self, ignore_names: list):
        """
        添加忽略的文件(夹)名,被忽略的文件(夹)不会显示在目录树中
        :param ignore_names: 忽略的文件(夹)名
        :return: None
        """
        if self.__generate_flag:
            raise ValueError("ignore_names cannot be set after drawing")
        for item in ignore_names:
            if item.startswith("*"):
                self.__kwargs["ignore_suffix"].append(item[1:])
            else:
                self.__kwargs["ignore_names"].append(item)

    def add_zip_suffix(self, zip_suffix: list, minimum: int = 0):
        """
        添加要压缩的后缀名，被压缩的文件会显示为...(.后缀名)
        :param zip_suffix: 要压缩的后缀名
        :param minimum: 当文件夹中后缀为zip_suffix的文件数小于minimum时，不会在目录树中压缩显示
        :return: None
        """
        if self.__generate_flag:
            raise ValueError("zip_suffix cannot be set after drawing")
        for item in zip_suffix:
            if not item.startswith("."):
                raise ValueError("zip_suffix must start with '.'")
        self.__kwargs["zip_suffix"].extend(zip_suffix)
        self.__kwargs["zip_suffix_minimum"] = minimum

    def __preprocess(self, path: str):
        """
        预处理
        :param path: 目录路径
        :return: 文件(夹)名列表
        """
        filenames_list = os.listdir(path)
        result_list = []
        zip_dict: dict[str, list[str]] = {}
        for item in filenames_list:
            # 忽略的文件(夹)名
            if item in self.__kwargs["ignore_names"] or item.endswith(
                tuple(self.__kwargs["ignore_suffix"])
            ):
                continue
            # 文件夹
            if os.path.isdir(os.path.join(path, item)):
                result_list.append(item)
                continue
            # 压缩的后缀名
            suffix = "." + item.split(".")[-1]
            if suffix not in self.__kwargs["zip_suffix"]:
                # 不压缩
                result_list.append(item)
                continue
            # 压缩
            suffix_list = zip_dict.get(suffix, [])
            if len(suffix_list) == 1 and suffix_list[0] == f"...({suffix})":
                continue
            if len(suffix_list) >= self.__kwargs["zip_suffix_minimum"] - 1:
                suffix_list.clear()
                suffix_list.append(f"...({suffix})")
            else:
                suffix_list.append(item)
            zip_dict[suffix] = suffix_list
        # 合并
        for _, value in zip_dict.items():
            result_list.extend(value)
        return result_list

    def __generate_file_tree(self, path: str, depth: int):
        """
        递归打印文件目录树状图
        :param path: 根目录路径
        :param depth: 根目录、文件所在的层级号
        :return: None
        """
        filenames_list = self.__preprocess(path)
        void_num = 0
        for item in filenames_list:
            # 计算当前文件(夹)的缩进
            string_list = ["│   " for _ in range(depth - void_num - len(self.__site))]
            for s in self.__site:
                string_list.insert(s, "    ")
            # 判断当前文件(夹)是否为最后一个
            if item != filenames_list[-1]:
                # 本级目录非最后一个文件：竖线
                string_list.append("├── ")
            else:
                # 本级目录最后一个文件：转折处
                string_list.append("└── ")
                void_num += 1
                # 添加当前已出现转折的层级数
                self.__site.append(depth)
            # 记录文件(夹)名
            self.__output += "".join(string_list) + item + "\n"
            # 递归
            new_item = os.path.join(path, item)
            if os.path.isdir(new_item) and (
                depth < self.__kwargs["max_depth"] - 1
                or self.__kwargs["max_depth"] == -1
            ):
                self.__generate_file_tree(new_item, depth + 1)
            if item == filenames_list[-1]:
                void_num -= 1
                # 移除当前已出现转折的层级数
                self.__site.pop()


if __name__ == "__main__":
    file_tree = FileTreeGenerator(
        r"E:\CodeField\CODE_PY\ToolsCollection\app",
        max_depth=3,
        ignore_names=["__pycache__", ".idea", ".git", ".gitignore", "users", "*.ui"],
        zip_suffix=[".png", ".svg", "ll"],
        zip_suffix_minimum=4,
    )
    file_tree.draw()
