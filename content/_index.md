---
title: "BALZER LAB"
summary: "Research group in nephrology studying how kidney cells adapt, recover, and fail in disease using single-cell multi-omics."
description: "The BALZER LAB investigates molecular mechanisms of kidney disease, fibroinflammatory niches, and translational single-cell multi-omics to advance precision nephrology."
title_seo: "BALZER LAB"
date: 2026-01-20
type: landing

sections:
  # 1) Full-bleed custom slider + global CSS for slider + hero tweaks
  - block: markdown
    content:
      title: ""
      text: |
        {{< rawhtml >}}
        <style>
          :root {
            /* HERO LOGO SIZE */
            --hb-hero-logo-h: 450px;
            --hb-hero-logo-h-mobile: 220px;
          }

          /* -------------------------------------------------------------------------- */
          /* SLIDER                                                                      */
          /* -------------------------------------------------------------------------- */

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

          .hb-indicators {
            position: absolute;
            left: 0;
            right: 0;
            bottom: 14px;
            display: flex;
            justify-content: center;
            gap: 10px;
            z-index: 5;
            padding: 0;
            margin: 0;
            list-style: none;
            pointer-events: none;
          }

          .hb-indicators button {
            pointer-events: auto;
            width: 38px;
            height: 10px;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.65);
            background: rgba(255,255,255,0.25);
            backdrop-filter: blur(6px);
            cursor: pointer;
          }

          .hb-indicators button[aria-current="true"] {
            background: rgba(255,255,255,0.85);
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
            user-select: none;
          }

          .hb-nav.prev { left: 14px; }
          .hb-nav.next { right: 14px; }

          /* -------------------------------------------------------------------------- */
          /* HERO V-CENTER                                                               */
          /* -------------------------------------------------------------------------- */

          .hero-vcenter .row {
            align-items: center;
          }

          .hero-vcenter .container,
          .hero-vcenter .container-fluid {
            padding-top: 0;
            padding-bottom: 0;
          }

          .hero-vcenter .hero-content,
          .hero-vcenter .hero-lead,
          .hero-vcenter .hero-text,
          .hero-vcenter .hero-media,
          .hero-vcenter .hero-image {
            margin-top: 0;
            margin-bottom: 0;
            padding-top: 0;
            padding-bottom: 0;
          }

          .hero-vcenter .hero-media img,
          .hero-vcenter .hero-image img,
          .hero-vcenter img {
            display: block;
            margin: 0 auto;
          }

          /* -------------------------------------------------------------------------- */
          /* FORCE HERO TEXT COLUMN TO HAVE HEIGHT                                       */
          /* -------------------------------------------------------------------------- */

          .hb-hero-compact .hero-content,
          .hb-hero-compact .hero-content .row,
          .hb-hero-compact .hero-content [class*="col"] {
            height: 100%;
          }

          /* -------------------------------------------------------------------------- */
          /* HERO TEXT: robust vertical centering via wrapper                            */
          /* -------------------------------------------------------------------------- */

          .hb-hero-compact .hb-hero-text {
            min-height: var(--hb-hero-logo-h);
            display: flex;
            flex-direction: column;
            justify-content: center;
          }

          @media (max-width: 768px) {
            .hb-hero-compact .hb-hero-text {
              min-height: unset;
              justify-content: flex-start;
            }
          }

          .hb-hero-compact .hero-media,
          .hb-hero-compact .hero-media figure,
          .hb-hero-compact .hero-media picture {
            max-height: none;
          }

          .hb-hero-compact .hero-media img,
          .hb-hero-compact .hero-media picture img {
            height: var(--hb-hero-logo-h);
            width: auto;
            max-height: none;
            max-width: 100%;
            object-fit: contain;
            display: block;
            margin: 0 auto;
          }

          @media (max-width: 768px) {
            .hb-hero-compact .hero-media img,
            .hb-hero-compact .hero-media picture img {
              height: var(--hb-hero-logo-h-mobile);
            }
          }
        </style>

        <div class="hb-fullbleed">
          <div class="hb-slider" id="hbHomeSlider">
            <div class="hb-slide is-active"><img src="/media/slide1.png" alt="Kidney research using single-cell omics"></div>
            <div class="hb-slide"><img src="/media/slide2.png" alt="Renal tissue and cellular microenvironment"></div>
            <div class="hb-slide"><img src="/media/slide3.png" alt="Fibroinflammatory niches in kidney disease"></div>
            <div class="hb-slide"><img src="/media/slide4.png" alt="Translational nephrology research"></div>

            <button class="hb-nav prev" type="button" aria-label="Previous slide">‹</button>
            <button class="hb-nav next" type="button" aria-label="Next slide">›</button>

            <ul class="hb-indicators" aria-label="Choose slide">
              <li><button type="button" aria-label="Slide 1" aria-current="true"></button></li>
              <li><button type="button" aria-label="Slide 2" aria-current="false"></button></li>
              <li><button type="button" aria-label="Slide 3" aria-current="false"></button></li>
              <li><button type="button" aria-label="Slide 4" aria-current="false"></button></li>
            </ul>
          </div>
        </div>

        <script>
          (function(){
            var root = document.getElementById('hbHomeSlider');
            if (!root) return;
            var slides = Array.prototype.slice.call(root.querySelectorAll('.hb-slide'));
            var dots = Array.prototype.slice.call(root.querySelectorAll('.hb-indicators button'));
            var prev = root.querySelector('.hb-nav.prev');
            var next = root.querySelector('.hb-nav.next');
            var i = 0;
            var timer = null;
            var intervalMs = 4500;

            function show(n){
              i = (n + slides.length) % slides.length;
              slides.forEach(function(s,k){
                s.classList.toggle('is-active', k === i);
              });
              dots.forEach(function(d,k){
                d.setAttribute('aria-current', k === i ? 'true' : 'false');
              });
            }

            function start(){
              stop();
              timer = window.setInterval(function(){ show(i + 1); }, intervalMs);
            }

            function stop(){
              if (timer) window.clearInterval(timer);
              timer = null;
            }

            dots.forEach(function(d,k){
              d.addEventListener('click', function(){
                show(k);
                start();
              });
            });

            if (prev) prev.addEventListener('click', function(){ show(i - 1); start(); });
            if (next) next.addEventListener('click', function(){ show(i + 1); start(); });

            root.addEventListener('mouseenter', stop);
            root.addEventListener('mouseleave', start);
            start();
          })();
        </script>
        {{< /rawhtml >}}
    design:
      spacing:
        padding: ["0", "0", "0", "0"]

  # 2) Hero
  - block: hero
    content:
      image:
        filename: balzerlab.png
      text: |
        <div class="hb-hero-text">
          We uncover how kidney cells <strong>adapt, recover, and fail</strong> in disease.
          Using <strong>single-cell multi-omics</strong>, we drive early diagnosis, precise classification,
          and personalized therapies for <strong>kidney disorders</strong>.
        </div>
    design:
      css_class: hb-hero-compact hero-vcenter
      spacing:
        padding: ["1rem", "0", "1rem", "0"]
---
