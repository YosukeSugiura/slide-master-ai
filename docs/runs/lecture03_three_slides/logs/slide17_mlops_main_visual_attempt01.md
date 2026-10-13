# Slide 17 MLOps illustration generation — attempt 01

- Outcome: **FAIL**; do not integrate or claim a completed slide.
- Trigger: User issued 「次」 after prior assistant explicitly said next production target was slide 17. This is a **separate production attempt**, not step E03 of the A/B/C comparison. The GitHub experimental STATE remains E03 READY.
- Requirements: standalone integrated main infographic of MLOps lifecycle; Collection → Preprocessing → Training → Evaluation → Deployment → Monitoring, with monitoring-driven retraining/update and redeployment, as defined by docs/lecture03_48_selected_3_contents.md (Slide 17); no slide title, Intro, Takeaway or body text inside image; editable PPTX text would be a later step.
- Actual image: a complete Japanese lecture slide, including a large slide heading, prose in four panels and a bottom Takeaway; not a standalone illustration. The generated 4-panel representation also did not clearly distinguish every required node/feedback route.
- Tool-observable output: generated PNG in the current ChatGPT conversation, named a_clean_educational_presentation_slide_in_japanese.png. **Binary not uploaded to GitHub**. This is a user-visible failed output, not an accepted asset.
- Root cause: exact prompt delivered internally to the image renderer is unobservable; the tool's returned description implies the objective was reinterpreted as a Japanese lecture slide. Do not assert the submitted standalone-illustration text was passed verbatim.
- Evaluation: independence FAIL; scope FAIL; editable-label separation FAIL; semantic cycle verification FAIL. Do not assign aesthetic scores as evidence of acceptance.
- Next: retry only after isolating visual-only generation instructions and validating observable input; maximum 3 attempts per asset. Do not substitute cropped content from the failed full-slide image or silently switch to constructed PPTX arrows.
