**Design System Technical Specification: FAQ Recommendations Frontend**

This document complements the Frontend Requirements Document for the FAQ Recommendations application and defines the style guidelines to ensure a consistent and modern UI.

**1. Color Palette**

* **Primary Colors:**

    | Color Name       | Hex Code  | Usage                                  |
    | :----------------- | :-------- | :------------------------------------- |
    | Primary Purple     | `#6400E4` | Search button, interactive elements    |
    | Background Beige   | `#FFF8F2` | Page background (optional)             |
    | Accent Yellow      | `#FFD300` | Highlight (can be used for alerts)    |
    | Text Navy        | `#10162F` | Main text color                      |
* **Secondary Colors:**

    | Color Name | Hex Code  | Usage                                |
    | :---------- | :-------- | :----------------------------------- |
    | White      | `#FFFFFF` | Header background, search area, FAQs |
    | Light Gray | `#F6F6F6` | Selected item background (optional)  |
    | Green      | `#3CB371` | Relevance indicator (optional)     |
    | Blue       | `#3B82F6` | Relevance indicator (optional)     |
* **Gradients:**

    * If used for relevance indication:

        ```css
        /* Green gradient for high relevance */
        background-gradient: linear-gradient(to right, rgba(240, 253, 244, 1), transparent);
        
        /* Blue gradient for medium relevance */
        background-gradient: linear-gradient(to right, rgba(239, 246, 255, 1), transparent);
        ```

**2. Typography**

* **Font Family:**

    ```css
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    ```
* **Font Sizes:**

    | Element   | Size            | Weight | Line Height | Usage                               |
    | :-------- | :-------------- | :----- | :---------- | :---------------------------------- |
    | Heading 1 | 24px (1.5rem)   | 700    | 1.2         | Page title ("FAQ Recommendations")  |
    | Heading 2 | 20px (1.25rem)  | 700    | 1.2         | Section title (e.g., "FAQs from Selected FAQ") |
    | Heading 3 | 18px (1.125rem) | 700    | 1.3         | FAQ question                        |
    | Body      | 16px (1rem)     | 400    | 1.5         | FAQ answer                          |
    | Small     | 14px (0.875rem) | 400    | 1.5         | Secondary information               |
    | Label     | 14px (0.875rem) | 500    | 1.5         | Labels (e.g., "Question:", "Answer:") |

**3. Components**

* **Header:**

    ```css
    background-color: white;
    padding: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    ```

    * Title:

        ```css
        color: #10162F;
        font-size: 1.5rem;
        font-weight: 700;
        ```
    * Social Media Icons:

        ```css
        color: #6400E4;
        margin-left: 0.5rem; /* Space between icons */
        ```
* **Search Area:**

    ```css
    background-color: #FFFFFF;
    padding: 1rem;
    border-radius: 0.375rem;
    display: flex;
    align-items: center;
    ```

    * FAQ Selection Dropdown:

        ```css
        /* Default select styles */
        ```
    * Text Field:

        ```css
        flex-grow: 1;
        margin-right: 0.5rem; /* Space between field and button */
        /* Default input styles */
        ```
    * Search Button:

        ```css
        background-color: #6400E4;
        color: white;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        transition: background-color 150ms ease;
        ```

        * Hover state:

            ```css
            background-color: #5000B4;
            ```
* **FAQ List:**

    ```css
    margin-top: 1rem;
    ```

    * FAQ Item:

        ```css
        padding: 1rem;
        border-bottom: 1px solid #E6E6E6;
        ```

        * Question:

            ```css
            color: #10162F;
            font-size: 1.125rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            ```
        * Answer:

            ```css
            color: #10162F;
            font-size: 1rem;
            ```
        * Relevance Indicator (Optional):

            ```css
            /* Styles for the relevance bar/icon */
            ```

**4. Hover Effects & Animations**

* **Search Button:**

    ```css
    /* Already defined in the search area */
    ```
* **FAQ List Items:**

    * A subtle highlight on hover can be added if desired.

        ```css
        transition: background-color 0.15s ease-in-out;
        cursor: pointer;
        ```

        * Hover state:

            ```css
            background-color: #F6F6F6;
            ```
* **Animations:**

    * Use CSS transitions for smooth state changes (e.g., color, background).
    * Consider subtle animations when reordering the FAQ list (may require JavaScript).

**5. Responsive Behavior**

* **Breakpoints:**

    | Breakpoint | Width  | Description             |
    | :--------- | :----- | :---------------------- |
    | sm         | 640px  | Small devices (mobile)  |
    | md         | 768px  | Medium devices (tablets) |
    | lg         | 1024px | Large devices (desktops) |
    | xl         | 1280px | Extra large devices     |
* **Search Area Layout:**

    ```css
    /* Mobile (default) - Stack elements */
    flex-direction: column;
    align-items: stretch;
    
    /* Tablet and above - Align in a row */
    @media (min-width: 768px) {
      flex-direction: row;
      align-items: center;
    }
    ```
* **FAQ List:**

    * Ensure the FAQ list remains readable across different screen sizes.

**6. Accessibility Guidelines**

* **Color Contrast:**

    * Verify color contrast to ensure readability (especially important for `#10162F` text on `#FFFFFF` and `#FFF8F2` backgrounds, and `#FFFFFF` text on the `#6400E4` button).
* **Focus States:**

    ```css
    :focus {
      outline: 2px solid #6400E4;
      outline-offset: 2px;
    }
    ```
* **Semantic HTML:**

    * Use appropriate HTML elements (`<header>`, `<main>`, `<section>`, `<form>`, `<button>`, `<ul>`, `<li>`, etc.).
* **ARIA Attributes:**

    * Add `aria-label` to elements that may need description (e.g., social media icons).
    * Use `aria-current="page"` if there is navigation.
* **Keyboard Navigation:**

    * Ensure all interactive elements are keyboard accessible (tabbing, Enter key, etc.).

**7. Implementation Notes**

* Use CSS variables for colors and fonts to ease maintenance.
* Implement styles precisely, following size, spacing, and color specifications.
* Test the interface across different browsers and devices to ensure consistency.
* Utilize styling libraries and frameworks efficiently (e.g., Tailwind CSS, Material UI, if applicable).

This document provides a detailed guide for styling the FAQ Recommendations application's frontend, promoting a consistent and user-friendly experience.