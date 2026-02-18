---
title: "BALZER LAB | Molecular Nephrology and Kidney Disease Research"
title_seo: "BALZER LAB | Molecular Nephrology, Kidney Disease, Single-cell Multi-omics"
summary: "Nephrology-focused research group investigating the molecular mechanisms of kidney disease using single-cell multi-omics."
description: "The BALZER LAB is a nephrology-focused research group investigating the molecular mechanisms of kidney disease. We uncover how kidney cells adapt, recover, and fail in disease. Using single-cell multi-omics, we drive early diagnosis, precise classification, and personalized therapies for kidney disorders."
date: 2026-02-18
type: landing

sections:

  # 1) Full-bleed slider + CSS
  - block: markdown
    content:
      title: ""
      text: |
        {{< rawhtml >}}
        <style>
          :root {
            --hb-hero-logo-h: 450px;
            --hb-hero-logo-h-mobile: 220px;
          }

          .hb-home-h1{
            margin: 0 0 .6rem 0;
            line-height: 1.1;
          }

          .hb-fullbleed {
            width: 100vw;
            margin-left: calc(50% - 50vw);
            margin-right: calc(50% - 50vw);
          }

          .hb-slider {
            position: relative;
            height: 380px;
            overflow: hidden;
          }

          @media (max-width: 768px) {
            .hb-slider { height: 240px; }
          }

          .hb-slide {
            position: absolute;
            inset: 0;
            opacity: 0;
            transition: opacity 450ms ease;
          }

          .hb-slide.is-active { opacity: 1; }

          .hb-slide img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
          }

          .hb-nav {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            z-index: 6;
            width: 44px;
            height: 44px;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.55);
            background: rgba(255,255,255,0.18);
            display: grid;
            place-items: center;
            cursor: pointer;
          }

          .hb-nav.prev { left: 14px; }
          .hb-nav.next { right: 14px; }

          .hb-hero-compact .hb-hero-text {
            min-height: var(--hb-hero-logo-h);
            display: flex;
            flex-direction: column;
            justify-content: center;
          }

          @media (max-width: 768px) {
            .hb-hero-compact .hb-hero-text {
              min-height: unset;
            }
          }

          .hb-hero-compact .hero-media img {
            height: var(--hb-hero-logo-h);
            width: auto;
            max-width: 100%;
            object-fit: contain;
          }

          @media (max-width: 768px) {
            .hb-hero-compact .hero-media img {
              height: var(--hb-hero-logo-h-mobile);
            }
          }
        </style>

        <div class="hb-fullbleed">
          <div class="hb-slider" id="hbHomeSlider">

            <div class="hb-slide is-active">
              <img src="/media/slide1.png" alt="Single-cell nephrology research">
            </div>
            <div class="hb-slide">
              <img src="/media/slide2.png" alt="Renal tissue and cellular microenvironment">
            </div>
            <div class="hb-slide">
              <img src="/media/slide3.png" alt="Fibroinflammatory niches in kidney disease">
            </div>
            <div class="hb-slide">
              <img src="/media/slide4.png" alt="Translational nephrology research">
            </div>

            <button class="hb-nav prev" type="button">‹</button>
            <button class="hb-nav next" type="button">›</button>
          </div>
        </div>

        <script>
          (function(){
            var root = document.getElementById('hbHomeSlider');
            if (!root) return;
            var slides = Array.from(root.querySelectorAll('.hb-slide'));
            var prev = root.querySelector('.hb-nav.prev');
            var next = root.querySelector('.hb-nav.next');
            var i = 0;
            function show(n){
              i = (n + slides.length) % slides.length;
              slides.forEach((s,k)=>s.classList.toggle('is-active',k===i));
            }
            prev.onclick=()=>show(i-1);
            next.onclick=()=>show(i+1);
          })();
        </script>
        {{< /rawhtml >}}
    design:
      spacing:
        padding: ["0", "0", "0", "0"]

  # 2) Hero with proper H1
  - block: hero
    content:
      image:
        filename: balzerlab.png
      text: |
        <div class="hb-hero-text">
          <h1 class="hb-home-h1">BALZER LAB</h1>

          <p>
            The BALZER LAB is a nephrology-focused research group investigating the molecular mechanisms of kidney disease.
          </p>
          <p>
            We uncover how kidney cells <strong>adapt, recover, and fail</strong> in disease.
          </p>
          <p>
            Using <strong>single-cell multi-omics</strong>, we drive early diagnosis, precise classification,
            and personalized therapies for <strong>kidney disorders</strong>.
          </p>
        </div>
    design:
      css_class: hb-hero-compact hero-vcenter
      spacing:
        padding: ["1rem", "0", "1rem", "0"]

  # 3) Navigation buttons
  - block: markdown
    content:
      title: ""
      text: |
        <div class="home-nav-buttons text-center">
          <a class="btn btn-primary" href="/research/">Learn about our research →</a>
          <a class="btn btn-primary" href="/team/">Meet the team →</a>
          <a class="btn btn-primary" href="/publications/">Read our publications →</a>
          <a class="btn btn-primary" href="/news/">Get the latest news →</a>
          <a class="btn btn-primary" href="/contact/">Join our team →</a>
          <a class="btn btn-primary" href="/social/">Find us on Bluesky →</a>
        </div>

  # 4) Grants
  - block: markdown
    content:
      title: ""
      text: |
        {{< rawhtml >}}
        <div class="grants-section text-center">
          <p>We gratefully acknowledge funding and support from:</p>
          <div class="grants-logos">
            <img src="/media/logos/erc.png" alt="European Research Council">
            <img src="/media/logos/dfg.png" alt="German Research Foundation">
            <img src="/media/logos/ekfs.svg" alt="EKFS Foundation">
            <img src="/media/logos/jackstaedt.png" alt="Jackstädt Foundation">
            <img src="/media/logos/dgfn.svg" alt="German Society of Nephrology">
            <img src="/media/logos/daad.png" alt="DAAD">
            <img src="/media/logos/bihacademy.png" alt="BIH Academy">
            <img src="/media/logos/bihcsp.png" alt="BIH Clinician Scientist Program">
            <img src="/media/logos/sonnenfeld.png" alt="Sonnenfeld Foundation">
          </div>
        </div>
        {{< /rawhtml >}}

---
