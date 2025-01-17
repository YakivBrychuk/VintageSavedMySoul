# Testing Documentation for VintageSavedMySoul

## Table of Contents
1. [Introduction](#introduction)  
2. [Testing Approach](#testing-approach)  
3. [Tools Used](#tools-used)  
4. [Key Tests Summary](#key-tests-summary)  
5. [Browser & Device Checks](#browser--device-checks)  
6. [Known Gaps & Future Plans](#known-gaps--future-plans)  
7. [Conclusion](#conclusion)

---

## Introduction
This document provides a **high-level overview** of the testing conducted for **VintageSavedMySoul**, an e-commerce platform offering curated vintage and handmade products. Due to **time constraints**, a fully detailed set of test results and coverage data was **not** completed as planned. 

The information below outlines what testing **was** done, which tools were used, and where additional work is needed.

---

## Testing Approach

1. **Manual Smoke Testing**  
   - Verified that key pages (Home, Products, Product Detail, Favorites, and Checkout) load correctly without crashing.
   - Checked if adding items to favorites and cart worked under normal conditions.
   - Confirmed basic layout consistency and link navigations.


   ![Proof](</github_assets/testing_images/1.png>)
   ![Proof](</github_assets/testing_images/2.png>)
   ![Proof](</github_assets/testing_images/3.png>)
   ![Proof](</github_assets/testing_images/4.png>)
   ![Proof](</github_assets/testing_images/5.png>)
   ![Proof](</github_assets/testing_images/6.png>)
   ![Proof](</github_assets/testing_images/7.png>)
   ![Proof](</github_assets/testing_images/8.png>)
   ![Proof](</github_assets/testing_images/9.png>)
   ![Proof](</github_assets/testing_images/10.png>)
   ![Proof](</github_assets/testing_images/11.png>)
   ![Proof](</github_assets/testing_images/12.png>)
   ![Proof](</github_assets/testing_images/13.png>)
   ![Proof](</github_assets/testing_images/14.png>)
   ![Proof](</github_assets/testing_images/15.png>)

   

2. **Limited Unit & Integration Tests**  
   - Initially planned more comprehensive test coverage, but only a few Django app tests were written (e.g., minimal views and forms tests).
   - No final coverage report is available due to incomplete integration of all test modules.

3. **Ad-hoc User Testing**  
   - Shared the site link with a few friends; they provided quick impressions of layout, ease of use, and basic functionality.
   - Gathered a small set of feedback on responsiveness and aesthetic.

Despite not achieving in-depth coverage, the above steps did reveal and fix minor bugs, ensuring the main site flows remain functional.

---

## Tools Used

- **Django Test Framework**: Some partial tests for model methods and view responses.  
- **Browser Developer Tools** (Chrome, Firefox): Checked for console errors, verified responsive layout at various screen sizes.  
- **Real Devices**: Quick checks on an iPhone (Safari) and an Android phone (Chrome).  
- **Manual Observations**: Simple user interactions to confirm no major breakage.

*(No formal CI environment or coverage tools, like `coverage.py`, were fully set up for final reporting.)*

---

## Key Tests Summary

1. **Home & Navbar**  
   - Confirmed that the homepage loads, the navbar toggles in mobile view, and links to login/favorites/cart are accessible.

2. **Products Page**  
   - Ensured product listing grid displays items with images/prices/categories.
   - Sorting dropdown tested (price, rating, etc.), appearing to work under normal usage.

3. **Favorites**  
   - Logged-in user toggled heart icons on multiple products. Confirmed the “My Favorites” page updated accordingly.
   - Guest user is prompted to log in when clicking the heart icon, as expected.

4. **Cart & Basic Checkout**  
   - Added item to cart, changed quantity, and briefly checked the partial checkout form. 
   - No extensive payment integration tests performed; no real orders were placed.

5. **Footer & Mobile Responsiveness**  
   - Footer displayed correctly in both desktop and mobile screens. Minor spacing issues corrected.

---

## Browser & Device Checks

- **Desktop**: Chrome (Windows), Firefox (Windows). Pages loaded, no major layout or script errors.  
- **Mobile**: iPhone Safari, Android Chrome. Layout scaled properly, minor spacing tweaks made.  
- **Tablet**: Limited testing on an iPad simulator; cart and favorites pages maintained acceptable layout.


---

## Known Gaps & Future Plans

1. **Automated Test Coverage**  
   - Currently minimal. Future work will include robust test suites (views, models, user flows) and coverage metrics.

2. **Stress & Performance Testing**  
   - Not performed. Need to see how the site behaves under high traffic or limited bandwidth.

3. **Accessibility Audits**  
   - Only did quick checks (e.g., alt tags, heading structure). Full WAVE/Lighthouse audits remain pending.

4. **SEO & Lighthouse Analysis**  
   - Quick Lighthouse run showed moderate performance. More in-depth optimization is desired (image compression, caching, etc.).

5. **Deployment Environment Quirks**  
   - With `DEBUG=False`, a few minor layout or image-loading issues popped up; those were only partially tested and fixed.

---

## Conclusion
While essential user flows of **VintageSavedMySoul** appear stable (browsing products, toggling favorites, partial checkout), **time constraints** limited our testing depth. **No** final coverage reports or exhaustive test logs exist. 

**Regrettably**, the lack of complete test results means we cannot definitively assure perfect reliability in all edge cases. However, the **core functionalities** were smoke-tested, and initial user feedback indicated a generally positive, functional experience. Future sprints will focus on **expanded automated testing**, deeper performance checks, and thorough accessibility compliance.

