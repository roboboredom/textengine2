## Welcome to GitHub Pages

You can use the [editor on GitHub](https://github.com/roboboredom/textengine2/edit/master/docs/index.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```python
# random variables
_integer = 10
_float = 172.322
_bool = True
_string = "Hello World!"

_list = [10, False, 10.2, 20, 10, "asd"]

_dict = {
  "apple"  : 10,
  "orange" : 20,
  "cherry" : 30
}

# random conditionals
while True:
  cmd = input("> ")
  if cmd == "exit":
    break
  elif cmd == "error":
    raise Exception("[ERROR] This is a test error.")
  else:
    print("Command \"", cmd, "\" is not valid.", sep="")

# random class
class Apple:
  """apple class docstring"""
  color = "red"
  weight = 10.0
  
  def __init__(self, isRipe=False):
    self.isRipe = isRipe
  
  def __str__(self):
    return "A " + self.red + " apple."
  
  @staticmethod
  def areApplesSame(a, b):
    if a.weight == b.weight and a.isRipe == b.isRipe:
      return True
    else:
      return False
```


For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/roboboredom/textengine2/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
