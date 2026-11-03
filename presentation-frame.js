/* Per-slide chapter labels and Team 4 details, shared by HTML and PDF export. */
(() => {
  const members = [
    ["Duk Pagnarith", "e20220184"],
    ["Leng Devid", "e20220888"],
    ["Hoeurn Sreyka", "e20220699"],
    ["Sou Pichchomrong", "e20221074"],
  ];

  function addSlideFrame() {
    const slides = [...document.querySelectorAll(".reveal .slides section.slide, .reveal .slides section#title-slide")];
    slides.forEach((slide, index) => {
      if (slide.querySelector(".slide-frame-header")) return;
      const title = slide.querySelector("h1, h2")?.textContent.trim() || "";
      const chapter = slide.dataset.chapter || "Presentation overview";
      const header = document.createElement("div");
      header.className = "slide-frame-header";
      const chapterLabel = document.createElement("span");
      chapterLabel.className = "chapter-label";
      chapterLabel.textContent = chapter;
      const slideLabel = document.createElement("span");
      slideLabel.className = "slide-label";
      slideLabel.textContent = index === 0 ? "Team 4" : title;
      header.append(chapterLabel, slideLabel);

      const footer = document.createElement("div");
      footer.className = "slide-frame-footer";
      const team = document.createElement("span");
      team.textContent = "Team 4";
      const course = document.createElement("span");
      course.className = "footer-topic";
      course.textContent = "Language Models for Information Retrieval";
      const number = document.createElement("span");
      number.textContent = `${index + 1} / ${slides.length}`;
      footer.append(team, course, number);
      slide.prepend(header);
      slide.append(footer);
    });

    const titleSlide = document.querySelector("#title-slide");
    if (titleSlide && !titleSlide.querySelector(".team-roster")) {
      const roster = document.createElement("div");
      roster.className = "team-roster";
      roster.setAttribute("aria-label", "Team 4 members and student IDs");
      members.forEach(([name, studentId]) => {
        const nameLabel = document.createElement("span");
        nameLabel.className = "team-member-name";
        nameLabel.textContent = name;
        const idLabel = document.createElement("span");
        idLabel.className = "team-member-id";
        idLabel.textContent = studentId;
        roster.append(nameLabel, idLabel);
      });
      titleSlide.querySelector(".quarto-title-authors")?.replaceWith(roster);
    }
    if (window.Reveal?.isReady()) window.Reveal.layout();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", addSlideFrame, { once: true });
  } else {
    addSlideFrame();
  }
})();
