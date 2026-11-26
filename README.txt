FAIRYYYYY NABUU — BIRTHDAY WEBSITE
==================================

A 6-screen birthday surprise that opens on a black starry cover and walks
through a letter, three memory pages and a final note.

  0  Cover      black + stars, "Welcome / Fairyyyy Nabuu", Enter button
  1  Letter     pink page, your words on a white card
  2  Memory 01  4 photos + a caption under each
  3  Memory 02  4 photos + a caption under each
  4  Memory 03  4 photos + a caption under each
  5  Last page  your final words + "Happy Birthday, Nabuu"

Navigation: Enter / Next / Back buttons, the dots at the bottom, a left or
right swipe on the phone, or the arrow keys on a computer.


1. PREVIEW
----------
Open index.html in any browser. Nothing to install, no internet needed.


2. ADD YOUR WORDS
-----------------
Open index.html in a text editor and search for the placeholder text:

  "Your words will go here — page 1."   -> the letter (screen 1)
  "Your caption here."                  -> the 12 photo captions
  "Your final words will go here."      -> the last page (screen 5)

Replace them with your own text. Keep the surrounding tags, only change the
words. Plain text is fine; use <br> for a line break inside a card.


3. ADD YOUR PHOTOS
------------------
Put the photos in this folder:

  assets/photos/photo-01.jpg   ... photo-12.jpg

Then, for each of the 12 placeholders in index.html, replace the placeholder
box with an image tag. Example for photo 01:

  BEFORE
    <div class="pbox" data-photo="01"><span class="ph-ico">📷</span><span>Photo 01</span></div>

  AFTER
    <div class="pbox" data-photo="01">
      <img src="assets/photos/photo-01.jpg" alt="Us on the rooftop">
    </div>

The caption goes in the <figcaption class="cap"> line right below it.
Tap a photo in the site and it opens full screen.

Recommended: 1200px wide or larger, JPG or WebP, roughly 150-300 KB each,
so the page stays fast on a phone.


4. PUBLISH IT FREE (so she can open the link)
---------------------------------------------
  1. Go to https://app.netlify.com/drop
  2. Drag this whole folder (or a ZIP of it) onto the page
  3. Netlify gives you a public link - send that link to her

The link is unlisted: it will not show up in search engines, but anyone who
has the link can open it. A passcode can be added later if you want one.


5. KEEP IT FOREVER
------------------
  - Save the published link somewhere safe.
  - Keep a copy of this whole folder as a backup.
  - For a copy that cannot ever go offline: open index.html in a browser,
    print it, and choose "Save as PDF". The print layout puts every screen
    on its own page, so the photos and words stay together as a keepsake.


6. FILES
--------
  index.html                 the whole website (structure, styles, script)
  assets/photos/             your 12 photos (created when you add them)
  README.txt                 this file
