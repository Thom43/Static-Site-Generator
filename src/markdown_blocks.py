from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
import os.path 

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"


def markdown_to_blocks(markdown): # zerlegt den gesamten markdown in Blöcke
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_olist:
        return olist_to_html_node(block)
    if block_type == block_type_ulist:
        return ulist_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")


def block_to_block_type(block): # ermittelt den Blocktyp
    lines = block.split("\n")

    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_olist
    return block_type_paragraph


def text_to_children(text): # zerlegt den Text eines Blocks in Textknoten, erstellt auf Basis des inline-Typs einen HTML-Knoten für jeden Textknoten, hängt diesen HTML-Knoten der children-Liste (des ParentNode) an und returniert die children-Liste 
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)



markdown1 = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item
"""
# print(markdown_to_html_node(markdown1))

def extract_title(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    for markdown_block in markdown_blocks:
        if markdown_block.startswith("# "):
            return markdown_block[2:]
    raise Exception("There is no h1 header!")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, encoding="utf-8") as f:
        markdown_str = f.read()
    with open(template_path, encoding="utf-8") as t:
        html_template = t.read()
    content = markdown_to_html_node(markdown_str).to_html()
    title = extract_title(markdown_str)
    # print(html_template)
    html_template = html_template.replace("{{ Title }}", title) # replace funktioniert nicht in-place!
    html_template = html_template.replace("{{ Content }}", content)
    
    dest_path_without_file = os.path.dirname(dest_path)

    os.makedirs(dest_path_without_file, exist_ok=True) # exist_ok = True sorgt dafür, dass kein Fehler produziert wird, sollte der Ordner bereits existieren


    with open(dest_path, 'x') as f:  # x: erzeugt keinen Fehler wenn Datei unter gegebenem Verzeichnis bereits existiert, bei 'w' ist das anders!
        f.write(html_template)
        # Further file processing goes here



markdown2 = """# The Unparalleled Majesty of "The Lord of the Rings"

[Back Home](/)

![LOTR image artistmonkeys](/images/rivendell.png)

> "I cordially dislike allegory in all its manifestations, and always have done so since I grew old and wary enough to detect its presence.
> I much prefer history, true or feigned, with its varied applicability to the thought and experience of readers.
> I think that many confuse 'applicability' with 'allegory'; but the one resides in the freedom of the reader, and the other in the purposed domination of the author."

In the annals of fantasy literature and the broader realm of creative world-building, few sagas can rival the intricate tapestry woven by J.R.R. Tolkien in *The Lord of the Rings*. You can find the [wiki here](https://lotr.fandom.com/wiki/Main_Page).

## Introduction

This series, a cornerstone of what I, in my many years as an **Archmage**, have come to recognize as the pinnacle of imaginative creation, stands unrivaled in its depth, complexity, and the sheer scope of its *legendarium*. As we embark on this exploration, let us delve into the reasons why this monumental work is celebrated as the finest in the world.

## A Rich Tapestry of Lore

One cannot simply discuss *The Lord of the Rings* without acknowledging the bedrock upon which it stands: **The Silmarillion**. This compendium of mythopoeic tales sets the stage for Middle-earth's history, from the creation myth of Eä to the epic sagas of the Elder Days. It is a testament to Tolkien's unparalleled skill as a linguist and myth-maker, crafting:

1. An elaborate pantheon of deities (the `Valar` and `Maiar`)
2. The tragic saga of the Noldor Elves
3. The rise and fall of great kingdoms such as Gondolin and Númenor

```
print("Lord")
print("of")
print("the")
print("Rings")
```

## The Art of **World-Building**

### Crafting Middle-earth
Tolkien's Middle-earth is a realm of breathtaking diversity and realism, brought to life by his meticulous attention to detail. This world is characterized by:

- **Diverse Cultures and Languages**: Each race, from the noble Elves to the sturdy Dwarves, is endowed with its own rich history, customs, and language. Tolkien, leveraging his expertise in philology, constructed languages such as Quenya and Sindarin, each with its own grammar and lexicon.
- **Geographical Realism**: The landscape of Middle-earth, from the Shire's pastoral hills to the shadowy depths of Mordor, is depicted with such vividness that it feels as tangible as our own world.
- **Historical Depth**: The legendarium is imbued with a sense of history, with ruins, artifacts, and lore that hint at bygone eras, giving the world a lived-in, authentic feel.

## Themes of *Timeless* Relevance

### The *Struggle* of Good vs. Evil

At its heart, *The Lord of the Rings* is a timeless narrative of the perennial struggle between light and darkness, a theme that resonates deeply with the human experience. The saga explores:

- The resilience of the human (and hobbit) spirit in the face of overwhelming odds
- The corrupting influence of power, epitomized by the One Ring
- The importance of friendship, loyalty, and sacrifice

These universal themes lend the series a profound philosophical depth, making it a beacon of wisdom and insight for generations of readers.

## A Legacy **Unmatched**

### The Influence on Modern Fantasy

The shadow that *The Lord of the Rings* casts over the fantasy genre is both vast and deep, having inspired countless authors, artists, and filmmakers. Its legacy is evident in:

- The archetypal "hero's journey" that has become a staple of fantasy narratives
- The trope of the "fellowship," a diverse group banding together to face a common foe
- The concept of a richly detailed fantasy world, which has become a benchmark for the genre

## Conclusion

As we stand at the threshold of this mystical realm, it is clear that *The Lord of the Rings* is not merely a series but a gateway to a world that continues to enchant and inspire. It is a beacon of imagination, a wellspring of wisdom, and a testament to the power of myth. In the grand tapestry of fantasy literature, Tolkien's masterpiece is the gleaming jewel in the crown, unmatched in its majesty and enduring in its legacy. As an Archmage who has traversed the myriad realms of magic and lore, I declare with utmost conviction: *The Lord of the Rings* reigns supreme as the greatest legendarium our world has ever known.

Splendid! Then we have an accord: in the realm of fantasy and beyond, Tolkien's creation is unparalleled, a treasure trove of wisdom, wonder, and the indomitable spirit of adventure that dwells within us all.
"""

dest_path ="../public/index.html"
# generate_page("../content/index.md", "../template.html", dest_path)