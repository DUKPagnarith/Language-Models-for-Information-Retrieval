#set heading(numbering: none)
#show heading: set text(fill: rgb("#107895"))
#show heading.where(level: 1): set text(size: 20pt, weight: "bold")
#show heading.where(level: 2): set text(size: 13pt, weight: "bold")
#set par(leading: 0.65em)
#set page(
  header: context [
    #set text(size: 9pt, fill: rgb("#52636b"))
    Language Models for IR #h(1fr) Team 4 / Learning guide
    #v(3pt)
    #line(length: 100%, stroke: 0.6pt + rgb("#107895"))
  ],
  footer: context [
    #line(length: 100%, stroke: 0.6pt + rgb("#107895"))
    #v(3pt)
    #align(right, text(size: 9pt, fill: rgb("#52636b"), counter(page).display("1 / 1", both: true)))
  ],
)
