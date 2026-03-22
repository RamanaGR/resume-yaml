#let name = "<<cv.name|escape_typst_characters>>"
#show heading.where(level: 1): it => [
#set text(
font: "<<design.header.name_font_family>>",
size: <<design.header.name_font_size>>,
weight: if <<design.header.name_bold|lower>> {630} else {440},
fill: design-colors-name,
)
#it.body
#v(<<design.header.vertical_space_between_name_and_connections>>)
]
= <<cv.name|escape_typst_characters>>
#let sep = <<design.header.connections.separator|escape_typst_characters>>
#align(<<design.header.alignment>>)[
((* for connection in cv.connections *))[<<connection["placeholder"]|escape_typst_characters>>]((* if not loop.last *))<<sep>>((* endif *))((* endfor *))
]
#v(<<design.header.vertical_space_between_connections_and_first_section>>)