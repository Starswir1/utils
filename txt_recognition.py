#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import yaml
import os
class FileSearcher:
    def __init__(self, config_file='config.xml'):
        """初始化搜索器"""
        self.config_file = config_file
        self.keywords = []
        self.directory = './'
        self.results = []
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                conf = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
                print(f"读取配置文件失败: {e}")
                return {}
            
        # 加载关键字
        keywords = conf['txt_recognition']['key_words']
        if keywords:
            for keyword in keywords.split(','):
                if keyword:
                    self.keywords.append(keyword.strip())
        
        # 加载搜索目录
        directory_elem = root.find('search/directory')
        if directory_elem and directory_elem.text:
            self.directory = directory_elem.text.strip()
        
        print(f"配置加载成功:")
        print(f"  搜索目录: {self.directory}")
        print(f"  搜索关键字: {', '.join(self.keywords)}")
        

    
    def search_files(self):
        """搜索文件"""
        if not os.path.exists(self.directory):
            print(f"错误: 目录 {self.directory} 不存在")
            return
        
        if not self.keywords:
            print("错误: 没有配置搜索关键字")
            return
        
        print(f"\n开始搜索目录: {self.directory}")
        
        # 遍历目录
        for root_dir, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root_dir, file)
                    self.search_in_file(file_path)
        
        self.print_results()
    
    def search_in_file(self, file_path):
        """在单个文件中搜索"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # 检查是否包含关键字
                found_keywords = []
                for keyword in self.keywords:
                    if keyword in content:
                        found_keywords.append(keyword)
                
                # 如果找到关键字，记录结果
                if found_keywords:
                    self.results.append({
                        'file_name': os.path.basename(file_path),
                        'file_path': file_path,
                        'keywords': found_keywords
                    })
                    
        except Exception as e:
            print(f"读取文件 {file_path} 失败: {e}")
    
    def print_results(self):
        """打印搜索结果"""
        print(f"\n搜索完成，共找到 {len(self.results)} 个匹配文件:")
        print("=" * 80)
        
        for i, result in enumerate(self.results, 1):
            print(f"\n{i}. 文件名: {result['file_name']}")
            print(f"   路径: {result['file_path']}")
            print(f"   匹配关键字: {', '.join(result['keywords'])}")
        
        print("=" * 80)

def main():
    """主函数"""
    searcher = FileSearcher()
    searcher.search_files()

if __name__ == '__main__':
    main()