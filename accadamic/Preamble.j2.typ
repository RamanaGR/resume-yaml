// Academic Dense Preamble
#import "@preview/fontawesome:0.5.0": fa-icon


#let locale-catalog-language = "<<locale.language>>"
#let design-text-font-family = "<<design.text.font_family>>"
#let design-text-font-size = <<design.text.font_size>>
#let design-text-leading = <<design.text.leading>>
#let design-text-alignment = "<<design.text.alignment>>"
#let design-colors-text = <<design.colors.text.as_rgb()>>
#let design-colors-section-titles = <<design.colors.section_titles.as_rgb()>>
#let design-colors-name = <<design.colors.name.as_rgb()>>
#let design-colors-connections = <<design.colors.connections.as_rgb()>>
#let design-page-size = "<<design.page.size>>"
#let design-page-top-margin = <<design.page.top_margin>>
#let design-page-bottom-margin = <<design.page.bottom_margin>>
#let design-page-left-margin = <<design.page.left_margin>>
#let design-page-right-margin = <<design.page.right_margin>>


// Page setup
#set page(
margin: (
top: design-page-top-margin,
bottom: design-page-bottom-margin,
left: design-page-left-margin,
right: design-page-right-margin,
),
paper: design-page-size,
)


// Text setup
#set text(
font: design-text-font-family,
size: design-text-font-size,
fill: design-colors-text,
lang: locale-catalog-language,
)
#set par(leading: design-text-leading)
