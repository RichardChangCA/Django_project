from django import template

register = template.Library()


@register.filter
def img_location(img_full_path):
    img_split = img_full_path.split("/")
    print("img_split", img_split)
    img_src = ""
    for i in range(len(img_split)):
        if i <= 2:
            continue
        else:
            img_src = img_src + "/" + img_split[i]
    print("img_src", img_src)
    img_name = "/" + img_src.split("/")[-3] + "/" + img_src.split("/")[-2] + "/" + \
               img_src.split("/")[-1]
    print("img_name", img_name)
    return img_name

#"/" + img_src.split("/")[-4] +
