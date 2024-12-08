CSS Cheat Sheet for NiceGUI

Layout

	•	w-full: Full width (100%).
	•	max-w-[size]: Max width (sm, md, lg, xl, 2xl, e.g., max-w-3xl).
	•	h-full: Full height (100%).
	•	flex: Makes the element a flex container.
	•	flex-[direction]: Flex direction (flex-row, flex-col, flex-row-reverse, flex-col-reverse).
	•	items-start: Align items to the start of the cross axis.
	•	items-center: Align items to the center of the cross axis.
	•	items-end: Align items to the end of the cross axis.
	•	items-baseline: Align items along the baseline of the cross axis.
	•	items-stretch: Stretch items to fill the cross axis.
	•	justify-start: Justify content to the start of the main axis.
	•	justify-center: Justify content to the center of the main axis.
	•	justify-between: Justify content with space between items along the main axis.
	•	justify-end: Justify content to the end of the main axis.
	•	justify-around: Justify content with space around items along the main axis.
	•	justify-evenly: Justify content with equal space between items along the main axis.

Spacing

	•	Margin vs Padding: 
		Margin is the space outside the border of an element, creating space between the element and its neighbors. 
		Padding is the space inside the border of an element, creating space between the content of the element and its border.

	•	m-[size]: Margin (m-0, m-2, m-4, etc.).
	•	mx-[size]: Horizontal margin (mx-auto, mx-4). (auto means automatic margin, centering the element horizontally)
	•	my-[size]: Vertical margin (my-0, my-4).
	•	p-[size]: Padding (p-2, p-4, etc.).
	•	px-[size]: Horizontal padding (px-4, px-6).
	•	py-[size]: Vertical padding (py-2, py-4).

Typography

	•	text-[size]: Text size (text-sm, text-lg, text-xl, text-2xl).
	•	font-[weight]: Font weight (font-light, font-bold, font-extrabold).
	•	leading-[size]: Line height (leading-tight, leading-loose).
	•	text-[alignment]: Text alignment (text-left, text-center, text-right).
	•	text-[color]: Text color (text-black, text-gray-700, text-blue-500).

Colors

	•	bg-[color]: Background color (bg-white, bg-gray-100, bg-blue-500).
	•	text-[color]: Text color (text-black, text-gray-700, text-red-500).
	•	border-[color]: Border color (border-black, border-gray-500).

Borders

	•	border: Adds a 1px solid border.
	•	border-[size]: Border size (border-2, border-4).
	•	rounded-[size]: Border radius (rounded-sm, rounded-md, rounded-lg, rounded-full).

Shadows

	•	shadow: Adds a default shadow.
	•	shadow-[size]: Shadow size (shadow-sm, shadow-md, shadow-lg).

Responsive Design

	•	sm:[class]: Small screen breakpoint (e.g., sm:w-1/2).
	•	md:[class]: Medium screen breakpoint (e.g., md:mx-4).
	•	lg:[class]: Large screen breakpoint (e.g., lg:py-6).
	•	xl:[class]: Extra-large screen breakpoint (e.g., xl:text-2xl).

Positioning

	•	relative: Sets the position to relative.
	•	absolute: Sets the position to absolute.
	•	fixed: Sets the position to fixed.
	•	top-[size]: Top position (top-0, top-4, top-8).
	•	left-[size]: Left position (left-0, left-4).
	•	right-[size]: Right position (right-0, right-4).

Miscellaneous

	•	hidden: Hides an element.
	•	block: Displays an element as a block.
	•	inline-block: Displays an element as an inline block.
	•	overflow-[behavior]: Overflow behavior (overflow-hidden, overflow-auto, overflow-scroll).