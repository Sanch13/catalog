/* Russian keyboard layouts
 * contains layout: 'russian-qwerty'
 *
 * To use:
 *  Point to this js file into your page header: <script src="layouts/russian.js" type="text/javascript"></script>
 *  Initialize the keyboard using: $('input').keyboard({ layout: 'russian-qwerty' });
 *
 * license for this file: WTFPL, unless the source layout site has a problem with me using them as a reference
 */

/* Thanks to Yury Kotlyarov (https://github.com/yura) */
$.keyboard.layouts['russian-qwerty'] = {
	'alt' : [
		"` 1 2 3 4 5 6 7 8 9 0 {bksp}",
		"q w e r t y u i o p [ ] \\",
		"a s d f g h j k l ; ' {accept}",
		"{shift} z x c v b n m , . @ - / ",
		"{enter} {alt} {space} {cancel}"
	],
	'alt-shift' : [
		'~ ! # $ % ^ & * ( ) _ {bksp}',
		"Q W E R T Y U I O P { } |",
		'A S D F G H J K L : " {accept}',
		"{shift} Z X C V B N M < > ? + =",
		"{enter} {alt} {space} {cancel}"
	],
	'default' : [
		"\u0451 1 2 3 4 5 6 7 8 9 0 {bksp}",
		"\u0439 \u0446 \u0443 \u043a \u0435 \u043d \u0433 \u0448 \u0449 \u0437 \u0445 \u044a \\",
		"\u0444 \u044b \u0432 \u0430 \u043f \u0440 \u043e \u043b \u0434 \u0436 \u044d {accept}",
		"{shift} \u044f \u0447 \u0441 \u043c \u0438 \u0442 \u044c \u0431 \u044e @ . - ",
		"{enter} {alt} {space} {cancel}"
	],
	'shift' : [
		'\u0401 ! " \u2116 ; \u20ac : ? * ( ) {bksp}',
		"\u0419 \u0426 \u0423 \u041a \u0415 \u041d \u0413 \u0428 \u0429 \u0417 \u0425 \u042a /",
		"\u0424 \u042b \u0412 \u0410 \u041f \u0420 \u041e \u041b \u0414 \u0416 \u042d {accept}",
		"{shift} \u042f \u0427 \u0421 \u041c \u0418 \u0422 \u042c \u0411 \u042e , + = ",
		"{enter} {alt} {space} {cancel}"
	]
};

$('button[data-action="accept"]').addClass('ui-accept-keyboard');

// Keyboard Language
// please update this section to match this language and email me with corrections!
// ***********************
if (typeof(language) === 'undefined') { var language = {}; };
language.russian = {
	display : {
		'a'      : '\u2714:Accept (Shift-Enter)', // check mark - same action as accept
		'accept' : 'Ввод:Accept (Shift-Enter)',
		'alt'    : 'РУС/ENG:Alternate Graphemes',
		'b'      : '\u2190:Backspace',    // Left arrow (same as &larr;)
		'bksp'   : '\u2B05:Backspace',  // version \u21D0 \u232B
		'c'      : '\u2716:Cancel (Esc)', // big X, close - same action as cancel
		'cancel' : 'Отмена:Cancel (Esc)',
		'clear'  : 'C:Clear',             // clear num pad
		'combo'  : '\u00f6:Toggle Combo Keys',
		'dec'    : '.:Decimal',           // decimal point for num pad (optional), change '.' to ',' for European format
		'e'      : '\u21b5:Enter',        // down, then left arrow - enter symbol
		'enter'  : 'Перевод строки:Enter',
		'lock'   : '\u21ea Lock:Caps Lock', // caps lock
		's'      : '\u21e7:Shift',        // thick hollow up arrow
		'shift'  : '\u2B06:Shift',
		'shift1'  : 'QQQ:Shift',
		'sign'   : '\u00b1:Change Sign',  // +/- sign for num pad
		'space'  : '&nbsp;:Space',
		't'      : '\u21e5:Tab',          // right arrow to bar (used since this virtual keyboard works with one directional tabs)
		'tab'    : '\u21e5 Tab:Tab'       // \u21b9 is the true tab symbol (left & right arrows)
	},
	// Message added to the key title while hovering, if the mousewheel plugin exists
	wheelMessage : 'Use mousewheel to see other keys',
};

// This will replace all default language options with these language options.
// it is separated out here so the layout demo will work properly.
$.extend(true, $.keyboard.defaultOptions, language.russian);


