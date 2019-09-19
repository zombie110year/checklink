# checklink

检查目录下的 Markdown 或 reStructruedText 中的链接

- reStructuredText 未实现


## 使用方法

```sh
checklink --target md path
```

递归地检查 `path` 目录下所有 markdown 文件中的链接.
当存在无法访问的链接时, 将打印在 stdout 中.

由于程序是单进程单线程的, 因此可能会很慢.

如果链接被识别为 http 链接, 则通过 request 发送一个请求.
如果是一个指向本地的链接, 则以 `path` 作为根目录测试此文件是否存在.

## Sequence

```
(FileSystem) -> FileIter -> path -> MarkdownParser -> Link -> Checker -> Result -> Output
```
