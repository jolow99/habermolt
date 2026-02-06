#import "@preview/fletcher:0.5.8" as fletcher: diagram, node, edge

// Color definitions
#let green = rgb("#4CAF50")
#let red = rgb("#F44336")
#let orange = rgb("#FF9800")
#let blue = rgb("#2196F3")
#let purple = rgb("#9C27B0")
#let light-purple = rgb("#E1BEE7")
#let light-blue = rgb("#BBDEFB")

// Document icon function
#let doc-icon(fill-color, lines: 3) = box(
  width: 12pt,
  height: 14pt,
  fill: fill-color.lighten(70%),
  stroke: fill-color + 0.5pt,
  radius: 1pt,
  inset: 2pt,
  {
    for i in range(lines) {
      place(
        top + left,
        dy: i * 3pt,
        rect(width: 7pt, height: 1.5pt, fill: fill-color)
      )
    }
  }
)

// Stack of document icons
#let doc-stack(colors) = stack(
  dir: ttb,
  spacing: 2pt,
  ..colors.map(c => doc-icon(c))
)

// Labeled statement box (purple AI-generated)
#let statement-box(lbl, msg) = box(
  fill: light-purple,
  stroke: purple + 0.5pt,
  radius: 2pt,
  inset: 4pt,
  stack(
    dir: ltr,
    spacing: 4pt,
    box(
      fill: purple,
      radius: 2pt,
      inset: (x: 4pt, y: 2pt),
      text(fill: white, weight: "bold", size: 8pt, lbl)
    ),
    text(size: 7pt, msg)
  )
)

// Ranking table
#let ranking-table(data) = {
  let header-colors = (green, red, orange, blue)
  table(
    columns: (auto,) + (12pt,) * 4,
    rows: 10pt,
    inset: 2pt,
    stroke: 0.5pt + gray,
    fill: (x, y) => if x > 0 and y == 0 { header-colors.at(x - 1).lighten(60%) },
    [], ..range(4).map(i => box(width: 8pt, height: 8pt, fill: header-colors.at(i).lighten(40%))),
    ..data.flatten().map(d => text(size: 7pt, if type(d) == int { str(d) } else { d }))
  )
}

// Section header
#let section-header(num, title) = align(center, stack(
  dir: ttb,
  spacing: 4pt,
  text(weight: "bold", size: 9pt, [#num. #title])
))

// Critique document
#let critique-doc(color, text-content) = box(
  fill: color.lighten(80%),
  stroke: color + 0.5pt,
  radius: 2pt,
  inset: 3pt,
  width: 50pt,
  text(size: 6pt, text-content)
)

// Main diagram
#set page(width: auto, height: auto, margin: 10pt)
#set text(font: "Helvetica", size: 8pt)

#box(stroke: blue + 1pt, radius: 4pt, inset: 8pt)[
  #text(weight: "bold", size: 10pt)[A]
  #h(20pt)
  #text(weight: "bold", size: 12pt)[Deliberation Protocol]

  #v(8pt)

  #grid(
    columns: (auto, auto, auto, auto, auto, auto, auto, auto, auto),
    column-gutter: 8pt,
    row-gutter: 4pt,
    align: center + horizon,

    // Row 1: Headers
    [],
    section-header(1, "Write Opinion"),
    [],
    section-header(2, [Rank \ Initial Statements]),
    [*Initial \ Winner*],
    section-header(3, "Write Critique"),
    [],
    section-header(4, [Rank \ Revised Statements]),
    [],

    // Row 2: Main content
    // Question box (vertical)
    rotate(-90deg, reflow: true, box(
      fill: light-blue,
      stroke: blue + 0.5pt,
      radius: 2pt,
      inset: 6pt,
      [*Question*]
    )),

    // Write Opinion section
    box(inset: 4pt)[
      #grid(
        columns: 2,
        column-gutter: 8pt,
        align: center,
        // People opinions
        stack(
          dir: ttb,
          spacing: 3pt,
          critique-doc(green, "No I don't feel..."),
          critique-doc(red, "I feel confident..."),
          critique-doc(orange, "What we need..."),
          critique-doc(blue, "I don't like..."),
          critique-doc(green, "We should..."),
        ),
        // Arrow and Habermas Machine output
        stack(
          dir: ttb,
          spacing: 4pt,
          box(
            fill: light-purple.lighten(50%),
            stroke: purple + 0.5pt,
            radius: 2pt,
            inset: 4pt,
          )[
            #doc-stack((green, red, orange, blue, green))
            #v(2pt)
            #sym.arrow.b
            #v(2pt)
            #text(size: 7pt, style: "italic", weight: "bold")[#smallcaps[Habermas Machine]]
            #text(size: 6pt)[ \ initial group statements]
          ],
          statement-box("A", "In our view, the..."),
          statement-box("B", "We feel that the..."),
          statement-box("C", "This is complex..."),
          statement-box("D", "The government..."),
        )
      )
    ],

    // Arrow
    sym.arrow.r,

    // Rank Initial Statements
    stack(
      dir: ttb,
      spacing: 8pt,
      ranking-table((
        ([A], 1, 2, 4, 2, 3),
        ([B], 2, 1, 1, 3, 2),
        ([C], 3, 2, 4, 2, 1),
        ([D], 4, 3, 3, 1, 1),
      )),
      text(weight: "bold", size: 8pt)[Aggregate & \ Select Winner],
      table(
        columns: 5,
        rows: 12pt,
        inset: 3pt,
        stroke: 0.5pt + gray,
        [3], [1], [4], [2],
      ),
      sym.arrow.b,
      box(
        fill: light-purple,
        stroke: purple + 1pt,
        radius: 2pt,
        inset: 4pt,
        [*B*]
      )
    ),

    // Initial Winner display
    rotate(-90deg, reflow: true, box(
      fill: light-blue,
      stroke: blue + 0.5pt,
      radius: 2pt,
      inset: 4pt,
      text(size: 7pt)[We feel that the...]
    )),

    // Write Critique section
    stack(
      dir: ttb,
      spacing: 3pt,
      critique-doc(green, "I agree that..."),
      critique-doc(red, "The statement..."),
      critique-doc(orange, "It's missing..."),
      critique-doc(blue, "Strike me as..."),
      critique-doc(green, "Appears sound..."),
    ),

    // Habermas Machine for revised statements
    box(
      fill: light-purple.lighten(50%),
      stroke: purple + 0.5pt,
      radius: 2pt,
      inset: 6pt,
    )[
      #grid(
        columns: 3,
        column-gutter: 4pt,
        align: center,
        [opinions], [+ initial winner], [+ critiques],
        doc-stack((green, red, orange, blue)),
        box(fill: light-purple, inset: 2pt, radius: 2pt, [B]),
        doc-stack((green, red, orange, blue)),
      )
      #v(4pt)
      #sym.arrow.b
      #v(2pt)
      #text(size: 7pt, style: "italic", weight: "bold")[#smallcaps[Habermas Machine]]
      #text(size: 6pt)[ \ revised group statements]
      #v(4pt)
      #grid(
        columns: 2,
        column-gutter: 4pt,
        row-gutter: 2pt,
        sym.arrow.r, statement-box("A", "We feel that the..."),
        sym.arrow.r, statement-box("B", "We strongly feel..."),
        sym.arrow.r, statement-box("C", "We first acknowledge..."),
        sym.arrow.r, statement-box("D", "We share the conviction..."),
      )
    ],

    // Rank Revised Statements
    stack(
      dir: ttb,
      spacing: 8pt,
      ranking-table((
        ([A], 3, 1, 3, 2, 4),
        ([B], 2, 2, 2, 1, 1),
        ([C], 2, 2, 1, 1, 3),
        ([D], 4, 3, 1, 2, 1),
      )),
      text(weight: "bold", size: 8pt)[Aggregate & \ Select Winner],
      table(
        columns: 5,
        rows: 12pt,
        inset: 3pt,
        stroke: 0.5pt + gray,
        [4], [3], [1], [2],
      ),
    ),

    // Final Preference
    stack(
      dir: ttb,
      spacing: 4pt,
      text(weight: "bold", size: 8pt)[5. Final Preference],
      grid(
        columns: 3,
        column-gutter: 8pt,
        align: center + horizon,
        box(fill: light-purple, inset: 4pt, radius: 2pt)[A],
        stack(
          dir: ttb,
          spacing: 2pt,
          text(size: 6pt)[initial #h(4pt) vs. #h(4pt) revised],
          text(size: 6pt)[winner #h(8pt) winner],
        ),
        box(fill: light-purple, inset: 4pt, radius: 2pt)[C],
      )
    ),
  )
]

#v(8pt)

// Legend
#box()[
  #text(weight: "bold")[B]
  #h(8pt)
  #box(width: 12pt, height: 12pt, fill: white, stroke: 0.5pt + gray)
  #text(size: 8pt)[ People generated]
  #h(16pt)
  #box(width: 12pt, height: 12pt, fill: light-purple, stroke: 0.5pt + purple)
  #text(size: 8pt)[ AI generated]
  #h(40pt)
  #text(weight: "bold")[C]
  #h(8pt)
  #text(size: 8pt)[Example final statement]
]
