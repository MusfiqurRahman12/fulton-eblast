import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Head CSS resets for iOS data detectors and body links
old_head_reset = """    a[x-apple-data-detectors], #MessageViewBody a { color: inherit !important; -webkit-text-fill-color: inherit !important; text-decoration: none !important; font-size: inherit !important; font-family: inherit !important; font-weight: inherit !important; line-height: inherit !important; }
    u + #body a { color: inherit; -webkit-text-fill-color: inherit; text-decoration: none; font-size: inherit; font-family: inherit; font-weight: inherit; line-height: inherit; }"""

new_head_reset = """    a[x-apple-data-detectors],
    a[x-apple-data-detectors] *,
    #MessageViewBody a,
    #MessageViewBody a *,
    .appleLinksWhite a,
    .appleLinksWhite a * {
      color: #FFFFFE !important;
      -webkit-text-fill-color: #FFFFFE !important;
      text-decoration: none !important;
      font-size: inherit !important;
      font-family: inherit !important;
      font-weight: inherit !important;
      line-height: inherit !important;
    }
    u + #body a,
    u + #body a * {
      color: #FFFFFE !important;
      -webkit-text-fill-color: #FFFFFE !important;
      text-decoration: none !important;
    }"""

if old_head_reset in html:
    html = html.replace(old_head_reset, new_head_reset)
else:
    print("Warning: old_head_reset not exact match, searching regex...")
    html = re.sub(r'a\[x-apple-data-detectors\].*?line-height: inherit; \}', new_head_reset, html, flags=re.DOTALL)

# 2. Section 6: Address & Date/Time
old_sec6 = """          <!-- ============================================
               SECTION 6: EVENT DETAILS (Address + Date/Time)
               ============================================ -->
          <tr>
            <td align="center" class="bg-body" bgcolor="#414446" style="background-color: #414446; background-image: linear-gradient(#414446, #414446); padding: 16px 40px 10px 40px;">
              <p class="c-white" style="margin: 0 0 8px 0; font-family: 'Plus Jakarta Sans', Arial, Helvetica, sans-serif; font-size: 15px; line-height: 22px; color: #FFFFFE; -webkit-text-fill-color: #FFFFFE; font-weight: 400; text-align: center;">
                <a href="https://maps.apple.com/?q=1220+2nd+Avenue+North+Nashville+TN+37208" target="_blank" style="color: #FFFFFE; -webkit-text-fill-color: #FFFFFE; text-decoration: none;">1220 2nd Avenue North, Nashville, TN 37208</a>
              </p>
              <p class="c-white" style="margin: 0; font-family: 'Plus Jakarta Sans', Arial, Helvetica, sans-serif; font-size: 18px; line-height: 26px; color: #FFFFFE; -webkit-text-fill-color: #FFFFFE; font-weight: 700; text-align: center; letter-spacing: 0.5px;">
                THURSDAY, OCTOBER 1ST<br />
                4:00 TO 6:00 PM
              </p>
            </td>
          </tr>"""

new_sec6 = """          <!-- ============================================
               SECTION 6: EVENT DETAILS (Address + Date/Time)
               ============================================ -->
          <tr>
            <td align="center" class="bg-body" bgcolor="#414446" style="background-color: #414446; background-image: linear-gradient(#414446, #414446); padding: 16px 40px 10px 40px;">
              <p class="c-white" style="margin: 0 0 8px 0; font-family: 'Plus Jakarta Sans', Arial, Helvetica, sans-serif; font-size: 15px; line-height: 22px; color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important; font-weight: 400; text-align: center;">
                <a href="https://maps.apple.com/?q=1220+2nd+Avenue+North+Nashville+TN+37208" target="_blank" style="color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important; text-decoration: none !important; border: 0 !important; outline: none !important;">
                  <span style="color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important; text-decoration: none !important; border-bottom: none !important;">1220 2nd Avenue North, Nashville, TN 37208</span>
                </a>
              </p>
              <p class="c-white" style="margin: 0; font-family: 'Plus Jakarta Sans', Arial, Helvetica, sans-serif; font-size: 18px; line-height: 26px; color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important; font-weight: 700; text-align: center; letter-spacing: 0.5px;">
                <span style="color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important;">THURSDAY, OCTOBER 1ST</span><br />
                <span style="color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important;">4:00 TO 6:00 PM</span>
              </p>
            </td>
          </tr>"""

html = html.replace(old_sec6, new_sec6)

# 3. Section 7: RSVP Button & Microcopy
old_sec7 = """                    <!--[if !mso]><!-->
                    <a href="mailto:info@liveatfulton.com?subject=I%20want%20to%20come%20to%20the%20event"
                       class="c-white bg-mauve btn-fluid"
                       style="display: inline-block; background-color: #8D5B5B; background-image: linear-gradient(#8D5B5B, #8D5B5B); color: #FFFFFE; -webkit-text-fill-color: #FFFFFE; font-family: 'Plus Jakarta Sans', Arial, Helvetica, sans-serif; font-size: 16px; font-weight: 700; line-height: 50px; text-align: center; text-decoration: none; width: 420px; max-width: 100%; letter-spacing: 3px; -webkit-text-size-adjust: none; padding: 0 10px;">
                      <span style="color: #FFFFFE; -webkit-text-fill-color: #FFFFFE;">RSVP TO ATTEND</span>
                    </a>
                    <!--<![endif]-->
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- RSVP Microcopy -->
          <tr>
            <td align="center" class="bg-body" bgcolor="#414446" style="background-color: #414446; background-image: linear-gradient(#414446, #414446); padding: 12px 40px 30px 40px;">
              <p class="c-white" style="margin: 0; font-family: 'Plus Jakarta Sans', Arial, Helvetica, sans-serif; font-size: 11px; line-height: 16px; color: #FFFFFE; -webkit-text-fill-color: #FFFFFE; font-weight: 700; letter-spacing: 3px; text-align: center;">
                SPACE IS LIMITED &nbsp;&bull;&nbsp; RSVP REQUIRED
              </p>
            </td>
          </tr>"""

new_sec7 = """                    <!--[if !mso]><!-->
                    <a href="mailto:info@liveatfulton.com?subject=I%20want%20to%20come%20to%20the%20event"
                       class="c-white bg-mauve btn-fluid"
                       style="display: inline-block; background-color: #8D5B5B; background-image: linear-gradient(#8D5B5B, #8D5B5B); color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important; font-family: 'Plus Jakarta Sans', Arial, Helvetica, sans-serif; font-size: 16px; font-weight: 700; line-height: 50px; text-align: center; text-decoration: none !important; width: 420px; max-width: 100%; letter-spacing: 3px; -webkit-text-size-adjust: none; padding: 0 10px;">
                      <span style="color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important; text-decoration: none !important;">RSVP TO ATTEND</span>
                    </a>
                    <!--<![endif]-->
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- RSVP Microcopy -->
          <tr>
            <td align="center" class="bg-body" bgcolor="#414446" style="background-color: #414446; background-image: linear-gradient(#414446, #414446); padding: 12px 40px 30px 40px;">
              <p class="c-white" style="margin: 0; font-family: 'Plus Jakarta Sans', Arial, Helvetica, sans-serif; font-size: 11px; line-height: 16px; color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important; font-weight: 700; letter-spacing: 3px; text-align: center;">
                <span style="color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important;">SPACE IS LIMITED &nbsp;&bull;&nbsp; RSVP REQUIRED</span>
              </p>
            </td>
          </tr>"""

html = html.replace(old_sec7, new_sec7)

# 4. Section 9: Reservations Copy
old_sec9 = """          <!-- ============================================
               SECTION 9: RESERVATIONS COPY
               ============================================ -->
          <tr>
            <td align="center" class="bg-body p-mob" bgcolor="#414446" style="background-color: #414446; background-image: linear-gradient(#414446, #414446); padding: 30px 40px 10px 40px;">
              <p class="c-white" style="margin: 0; font-family: 'Plus Jakarta Sans', Arial, Helvetica, sans-serif; font-size: 16px; line-height: 26px; color: #FFFFFE; -webkit-text-fill-color: #FFFFFE; font-weight: 400; text-align: center;">
                Fulton Residences is now accepting reservations,<br />
                with homes starting in the high $200s.
              </p>
            </td>
          </tr>"""

new_sec9 = """          <!-- ============================================
               SECTION 9: RESERVATIONS COPY
               ============================================ -->
          <tr>
            <td align="center" class="bg-body p-mob" bgcolor="#414446" style="background-color: #414446; background-image: linear-gradient(#414446, #414446); padding: 30px 40px 10px 40px;">
              <p class="c-white" style="margin: 0; font-family: 'Plus Jakarta Sans', Arial, Helvetica, sans-serif; font-size: 16px; line-height: 26px; color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important; font-weight: 400; text-align: center;">
                <span style="color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important;">Fulton Residences is now accepting reservations,<br />
                with homes starting in the high $200s.</span>
              </p>
            </td>
          </tr>"""

html = html.replace(old_sec9, new_sec9)

# 5. Section 10: Schedule a Private Presentation Button
old_sec10 = """                    <!--[if !mso]><!-->
                    <a href="mailto:info@liveatfulton.com?subject=I%20want%20to%20more%20information%20about%20Fulton"
                       class="c-white bg-mauve btn-fluid"
                       style="display: inline-block; background-color: #8D5B5B; background-image: linear-gradient(#8D5B5B, #8D5B5B); color: #FFFFFE; -webkit-text-fill-color: #FFFFFE; font-family: 'Plus Jakarta Sans', Arial, Helvetica, sans-serif; font-size: 14px; font-weight: 700; line-height: 50px; text-align: center; text-decoration: none; width: 480px; max-width: 100%; letter-spacing: 3px; -webkit-text-size-adjust: none; padding: 0 10px;">
                      <span style="color: #FFFFFE; -webkit-text-fill-color: #FFFFFE;">SCHEDULE A PRIVATE PRESENTATION</span>
                    </a>
                    <!--<![endif]-->"""

new_sec10 = """                    <!--[if !mso]><!-->
                    <a href="mailto:info@liveatfulton.com?subject=I%20want%20to%20more%20information%20about%20Fulton"
                       class="c-white bg-mauve btn-fluid"
                       style="display: inline-block; background-color: #8D5B5B; background-image: linear-gradient(#8D5B5B, #8D5B5B); color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important; font-family: 'Plus Jakarta Sans', Arial, Helvetica, sans-serif; font-size: 14px; font-weight: 700; line-height: 50px; text-align: center; text-decoration: none !important; width: 480px; max-width: 100%; letter-spacing: 3px; -webkit-text-size-adjust: none; padding: 0 10px;">
                      <span style="color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important; text-decoration: none !important;">SCHEDULE A PRIVATE PRESENTATION</span>
                    </a>
                    <!--<![endif]-->"""

html = html.replace(old_sec10, new_sec10)

# 6. Section 12: Explore Website (Bold White with Underline as per PDF)
old_sec12 = """          <!-- ============================================
               SECTION 12: EXPLORE WEBSITE CTA (Italic Copy)
               ============================================ -->
          <tr>
            <td align="center" class="bg-body p-mob" bgcolor="#414446" style="background-color: #414446; background-image: linear-gradient(#414446, #414446); padding: 0 40px 10px 40px;">
              <p class="c-white" style="margin: 0 0 16px 0; font-family: 'Plus Jakarta Sans', Arial, Helvetica, sans-serif; font-size: 16px; line-height: 26px; color: #FFFFFE; -webkit-text-fill-color: #FFFFFE; font-weight: 400; font-style: italic; text-align: center;">
                Visit our website to learn more about the community<br />
                and be among the first to receive updates.
              </p>
              <p style="margin: 0;">
                <a href="https://liveatfulton.com" target="_blank"
                   class="c-mauve"
                   style="font-family: 'Plus Jakarta Sans', Arial, Helvetica, sans-serif; font-size: 16px; line-height: 24px; color: #C49494; -webkit-text-fill-color: #C49494; font-weight: 800; text-decoration: underline; text-underline-offset: 3px;">
                  Explore Fulton Residences
                </a>
              </p>
            </td>
          </tr>"""

new_sec12 = """          <!-- ============================================
               SECTION 12: EXPLORE WEBSITE CTA (Italic Copy)
               ============================================ -->
          <tr>
            <td align="center" class="bg-body p-mob" bgcolor="#414446" style="background-color: #414446; background-image: linear-gradient(#414446, #414446); padding: 0 40px 10px 40px;">
              <p class="c-white" style="margin: 0 0 16px 0; font-family: 'Plus Jakarta Sans', Arial, Helvetica, sans-serif; font-size: 16px; line-height: 26px; color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important; font-weight: 400; font-style: italic; text-align: center;">
                <span style="color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important;">Visit our website to learn more about the community<br />
                and be among the first to receive updates.</span>
              </p>
              <p style="margin: 0;">
                <a href="https://liveatfulton.com" target="_blank"
                   class="c-white"
                   style="font-family: 'Plus Jakarta Sans', Arial, Helvetica, sans-serif; font-size: 17px; line-height: 24px; color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important; font-weight: 800; text-decoration: underline !important; text-underline-offset: 4px;">
                  <span style="color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important; text-decoration: underline !important;">Explore Fulton Residences</span>
                </a>
              </p>
            </td>
          </tr>"""

html = html.replace(old_sec12, new_sec12)

# 7. Section 14: Property Address
old_sec14 = """          <!-- ============================================
               SECTION 14: PROPERTY ADDRESS
               ============================================ -->
          <tr>
            <td align="center" class="bg-body" bgcolor="#414446" style="background-color: #414446; background-image: linear-gradient(#414446, #414446); padding: 26px 40px 30px 40px;">
              <p class="c-white" style="margin: 0; font-family: 'Plus Jakarta Sans', Arial, Helvetica, sans-serif; font-size: 13px; line-height: 18px; color: #FFFFFE; -webkit-text-fill-color: #FFFFFE; font-weight: 300; letter-spacing: 3px; text-align: center;">
                <a href="https://maps.apple.com/?q=1221+2nd+Ave+N+Nashville+TN+37208" target="_blank" style="color: #FFFFFE; -webkit-text-fill-color: #FFFFFE; text-decoration: none;">1221 2ND AVE N, NASHVILLE, TN 37208</a>
              </p>
            </td>
          </tr>"""

new_sec14 = """          <!-- ============================================
               SECTION 14: PROPERTY ADDRESS
               ============================================ -->
          <tr>
            <td align="center" class="bg-body" bgcolor="#414446" style="background-color: #414446; background-image: linear-gradient(#414446, #414446); padding: 26px 40px 30px 40px;">
              <p class="c-white" style="margin: 0; font-family: 'Plus Jakarta Sans', Arial, Helvetica, sans-serif; font-size: 13px; line-height: 18px; color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important; font-weight: 300; letter-spacing: 3px; text-align: center;">
                <a href="https://maps.apple.com/?q=1221+2nd+Ave+N+Nashville+TN+37208" target="_blank" style="color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important; text-decoration: none !important; border: 0 !important; outline: none !important;">
                  <span style="color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important; text-decoration: none !important; border-bottom: none !important;">1221 2ND AVE N, NASHVILLE, TN 37208</span>
                </a>
              </p>
            </td>
          </tr>"""

html = html.replace(old_sec14, new_sec14)

# 8. Section 4: Paragraphs & Headings in body copy
html = html.replace(
    '<p class="c-white" style="margin: 0 0 24px 0; font-family: \'Plus Jakarta Sans\', Arial, Helvetica, sans-serif; font-size: 14px; line-height: 20px; color: #FFFFFE; -webkit-text-fill-color: #FFFFFE;',
    '<p class="c-white" style="margin: 0 0 24px 0; font-family: \'Plus Jakarta Sans\', Arial, Helvetica, sans-serif; font-size: 14px; line-height: 20px; color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important;'
)
html = html.replace(
    '<p class="c-white" style="margin: 0 0 20px 0; font-family: \'Plus Jakarta Sans\', Arial, Helvetica, sans-serif; font-size: 16px; line-height: 26px; color: #FFFFFE; -webkit-text-fill-color: #FFFFFE;',
    '<p class="c-white" style="margin: 0 0 20px 0; font-family: \'Plus Jakarta Sans\', Arial, Helvetica, sans-serif; font-size: 16px; line-height: 26px; color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important;'
)
html = html.replace(
    '<p class="c-white" style="margin: 0 0 10px 0; font-family: \'Plus Jakarta Sans\', Arial, Helvetica, sans-serif; font-size: 16px; line-height: 26px; color: #FFFFFE; -webkit-text-fill-color: #FFFFFE;',
    '<p class="c-white" style="margin: 0 0 10px 0; font-family: \'Plus Jakarta Sans\', Arial, Helvetica, sans-serif; font-size: 16px; line-height: 26px; color: #FFFFFE !important; -webkit-text-fill-color: #FFFFFE !important;'
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: index.html fully reinforced with ultra-bulletproof dark mode locks!")
