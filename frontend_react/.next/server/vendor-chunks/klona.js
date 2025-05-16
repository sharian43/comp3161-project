"use strict";
/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
exports.id = "vendor-chunks/klona";
exports.ids = ["vendor-chunks/klona"];
exports.modules = {

/***/ "(ssr)/./node_modules/klona/json/index.mjs":
/*!*******************************************!*\
  !*** ./node_modules/klona/json/index.mjs ***!
  \*******************************************/
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   klona: () => (/* binding */ klona)\n/* harmony export */ });\nfunction klona(val) {\n\tvar k, out, tmp;\n\n\tif (Array.isArray(val)) {\n\t\tout = Array(k=val.length);\n\t\twhile (k--) out[k] = (tmp=val[k]) && typeof tmp === 'object' ? klona(tmp) : tmp;\n\t\treturn out;\n\t}\n\n\tif (Object.prototype.toString.call(val) === '[object Object]') {\n\t\tout = {}; // null\n\t\tfor (k in val) {\n\t\t\tif (k === '__proto__') {\n\t\t\t\tObject.defineProperty(out, k, {\n\t\t\t\t\tvalue: klona(val[k]),\n\t\t\t\t\tconfigurable: true,\n\t\t\t\t\tenumerable: true,\n\t\t\t\t\twritable: true,\n\t\t\t\t});\n\t\t\t} else {\n\t\t\t\tout[k] = (tmp=val[k]) && typeof tmp === 'object' ? klona(tmp) : tmp;\n\t\t\t}\n\t\t}\n\t\treturn out;\n\t}\n\n\treturn val;\n}\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKHNzcikvLi9ub2RlX21vZHVsZXMva2xvbmEvanNvbi9pbmRleC5tanMiLCJtYXBwaW5ncyI6Ijs7OztBQUFPO0FBQ1A7O0FBRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBLFlBQVk7QUFDWjtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLEtBQUs7QUFDTCxLQUFLO0FBQ0w7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFFQTtBQUNBIiwic291cmNlcyI6WyJDOlxcVXNlcnNcXHJqbXVuXFxEb3dubG9hZHNcXGNvbXAzMTYxLXByb2plY3QtbWFpblxcY29tcDMxNjEtcHJvamVjdC1tYWluXFxmcm9udGVuZFxcbm9kZV9tb2R1bGVzXFxrbG9uYVxcanNvblxcaW5kZXgubWpzIl0sInNvdXJjZXNDb250ZW50IjpbImV4cG9ydCBmdW5jdGlvbiBrbG9uYSh2YWwpIHtcblx0dmFyIGssIG91dCwgdG1wO1xuXG5cdGlmIChBcnJheS5pc0FycmF5KHZhbCkpIHtcblx0XHRvdXQgPSBBcnJheShrPXZhbC5sZW5ndGgpO1xuXHRcdHdoaWxlIChrLS0pIG91dFtrXSA9ICh0bXA9dmFsW2tdKSAmJiB0eXBlb2YgdG1wID09PSAnb2JqZWN0JyA/IGtsb25hKHRtcCkgOiB0bXA7XG5cdFx0cmV0dXJuIG91dDtcblx0fVxuXG5cdGlmIChPYmplY3QucHJvdG90eXBlLnRvU3RyaW5nLmNhbGwodmFsKSA9PT0gJ1tvYmplY3QgT2JqZWN0XScpIHtcblx0XHRvdXQgPSB7fTsgLy8gbnVsbFxuXHRcdGZvciAoayBpbiB2YWwpIHtcblx0XHRcdGlmIChrID09PSAnX19wcm90b19fJykge1xuXHRcdFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkob3V0LCBrLCB7XG5cdFx0XHRcdFx0dmFsdWU6IGtsb25hKHZhbFtrXSksXG5cdFx0XHRcdFx0Y29uZmlndXJhYmxlOiB0cnVlLFxuXHRcdFx0XHRcdGVudW1lcmFibGU6IHRydWUsXG5cdFx0XHRcdFx0d3JpdGFibGU6IHRydWUsXG5cdFx0XHRcdH0pO1xuXHRcdFx0fSBlbHNlIHtcblx0XHRcdFx0b3V0W2tdID0gKHRtcD12YWxba10pICYmIHR5cGVvZiB0bXAgPT09ICdvYmplY3QnID8ga2xvbmEodG1wKSA6IHRtcDtcblx0XHRcdH1cblx0XHR9XG5cdFx0cmV0dXJuIG91dDtcblx0fVxuXG5cdHJldHVybiB2YWw7XG59XG4iXSwibmFtZXMiOltdLCJpZ25vcmVMaXN0IjpbMF0sInNvdXJjZVJvb3QiOiIifQ==\n//# sourceURL=webpack-internal:///(ssr)/./node_modules/klona/json/index.mjs\n");

/***/ })

};
;