window.lazyLoadOptions={elements_selector:"img[data-lazy-src],.rocket-lazyload",data_src:"lazy-src",data_srcset:"lazy-srcset",data_sizes:"lazy-sizes",class_loading:"lazyloading",class_loaded:"lazyloaded",threshold:300,callback_loaded:function(t){"IFRAME"===t.tagName&&"fitvidscompatible"==t.dataset.rocketLazyload&&t.classList.contains("lazyloaded")&&void 0!==window.jQuery&&jQuery.fn.fitVids&&jQuery(t).parent().fitVids()}},window.addEventListener("LazyLoad::Initialized",function(t){var n=t.detail.instance;if(window.MutationObserver){var e=new MutationObserver(function(t){var e=0,a=0,r=0;t.forEach(function(t){for(i=0;i<t.addedNodes.length;i++){if("function"!=typeof t.addedNodes[i].getElementsByTagName||"function"!=typeof t.addedNodes[i].getElementsByClassName)return;images=t.addedNodes[i].getElementsByTagName("img"),is_image="IMG"==t.addedNodes[i].tagName,iframes=t.addedNodes[i].getElementsByTagName("iframe"),is_iframe="IFRAME"==t.addedNodes[i].tagName,rocket_lazy=t.addedNodes[i].getElementsByClassName("rocket-lazyload"),e+=images.length,a+=iframes.length,r+=rocket_lazy.length,is_image&&(e+=1),is_iframe&&(a+=1)}}),(e>0||a>0||r>0)&&n.update()}),a=document.getElementsByTagName("body")[0];e.observe(a,{childList:!0,subtree:!0})}},!1),function(t,n){"object"==typeof exports&&"undefined"!=typeof module?module.exports=n():"function"==typeof define&&define.amd?define(n):(t=t||self).LazyLoad=n()}(this,function(){"use strict";function t(){return(t=Object.assign||function(t){for(var n=1;n<arguments.length;n++){var e=arguments[n];for(var a in e)Object.prototype.hasOwnProperty.call(e,a)&&(t[a]=e[a])}return t}).apply(this,arguments)}var n="undefined"!=typeof window,e=n&&!("onscroll"in window)||"undefined"!=typeof navigator&&/(gle|ing|ro)bot|crawl|spider/i.test(navigator.userAgent),a=n&&"IntersectionObserver"in window,r=n&&"classList"in document.createElement("p"),o=n&&window.devicePixelRatio>1,l={elements_selector:"IMG",container:e||n?document:null,threshold:300,thresholds:null,data_src:"src",data_srcset:"srcset",data_sizes:"sizes",data_bg:"bg",data_bg_hidpi:"bg-hidpi",data_bg_multi:"bg-multi",data_bg_multi_hidpi:"bg-multi-hidpi",data_poster:"poster",class_applied:"applied",class_loading:"loading",class_loaded:"loaded",class_error:"error",unobserve_completed:!0,unobserve_entered:!1,cancel_on_exit:!1,callback_enter:null,callback_exit:null,callback_applied:null,callback_loading:null,callback_loaded:null,callback_error:null,callback_finish:null,callback_cancel:null,use_native:!1},s=function n(e){return t({},l,e)},c=function t(n,e){var a,r="LazyLoad::Initialized",o=new n(e);try{a=new CustomEvent(r,{detail:{instance:o}})}catch(l){(a=document.createEvent("CustomEvent")).initCustomEvent(r,!1,!1,{instance:o})}window.dispatchEvent(a)},u="loading",d="error",f="native",g="data-",v="ll-status",p=function t(n,e){return n.getAttribute(g+e)},b=function t(n,e,a){var r=g+e;if(null===a){n.removeAttribute(r);return}n.setAttribute(r,a)},h=function t(n){return p(n,v)},m=function t(n,e){return b(n,v,e)},y=function t(n){return m(n,null)},E=function t(n){return null===h(n)},z=function t(n){return h(n)===f},N=function t(n,e,a,r){if(n){if(void 0!==r){n(e,a,r);return}if(void 0!==a){n(e,a);return}n(e)}},I=function t(n,e){if(r){n.classList.add(e);return}n.className+=(n.className?" ":"")+e},L=function t(n,e){if(r){n.classList.remove(e);return}n.className=n.className.replace(RegExp("(^|\\s+)"+e+"(\\s+|$)")," ").replace(/^\s+/,"").replace(/\s+$/,"")},$=function t(n){n.llTempImage=document.createElement("IMG")},A=function t(n){delete n.llTempImage},k=function t(n){return n.llTempImage},_=function t(n,e){if(e){var a=e._observer;a&&a.unobserve(n)}},M=function t(n){n.disconnect()},O=function t(n,e,a){e.unobserve_entered&&_(n,a)},C=function t(n,e){n&&(n.loadingCount+=e)},R=function t(n){n&&(n.toLoadCount-=1)},x=function t(n,e){n&&(n.toLoadCount=e)},G=function t(n){for(var e,a=[],r=0;e=n.children[r];r+=1)"SOURCE"===e.tagName&&a.push(e);return a},T=function t(n,e,a){a&&n.setAttribute(e,a)},w=function t(n,e){n.removeAttribute(e)},B=function t(n){return!!n.llOriginalAttrs},F=function t(n){if(!B(n)){var e={};e.src=n.getAttribute("src"),e.srcset=n.getAttribute("srcset"),e.sizes=n.getAttribute("sizes"),n.llOriginalAttrs=e}},V=function t(n){if(B(n)){var e=n.llOriginalAttrs;T(n,"src",e.src),T(n,"srcset",e.srcset),T(n,"sizes",e.sizes)}},D=function t(n,e){T(n,"sizes",p(n,e.data_sizes)),T(n,"srcset",p(n,e.data_srcset)),T(n,"src",p(n,e.data_src))},P=function t(n){w(n,"src"),w(n,"srcset"),w(n,"sizes")},S=function t(n,e){var a=n.parentNode;a&&"PICTURE"===a.tagName&&G(a).forEach(e)},j=function t(n,e){G(n).forEach(e)},U=function t(n){S(n,function(t){V(t)}),V(n)},q=function t(n){S(n,function(t){P(t)}),P(n)},Q={IMG:function t(n,e){S(n,function(t){F(t),D(t,e)}),F(n),D(n,e)},IFRAME:function t(n,e){T(n,"src",p(n,e.data_src))},VIDEO:function t(n,e){j(n,function(t){T(t,"src",p(t,e.data_src))}),T(n,"poster",p(n,e.data_poster)),T(n,"src",p(n,e.data_src)),n.load()}},H=function t(n,e,a){var r=p(n,e.data_bg),l=p(n,e.data_bg_hidpi),s=o&&l?l:r;s&&(n.style.backgroundImage='url("'.concat(s,'")'),k(n).setAttribute("src",s),X(n,e,a))},J=function t(n,e,a){var r=p(n,e.data_bg_multi),l=p(n,e.data_bg_multi_hidpi),s=o&&l?l:r;s&&(n.style.backgroundImage=s,W(n,e,a))},K=function t(n,e){var a=Q[n.tagName];a&&a(n,e)},W=function t(n,e,a){I(n,e.class_applied),m(n,"applied"),tt(n,e),e.unobserve_completed&&_(n,e),N(e.callback_applied,n,a)},X=function t(n,e,a){C(a,1),I(n,e.class_loading),m(n,u),N(e.callback_loading,n,a)},Y={IMG:function t(n,e){b(n,e.data_src,null),b(n,e.data_srcset,null),b(n,e.data_sizes,null),S(n,function(t){b(t,e.data_srcset,null),b(t,e.data_sizes,null)})},IFRAME:function t(n,e){b(n,e.data_src,null)},VIDEO:function t(n,e){b(n,e.data_src,null),b(n,e.data_poster,null),j(n,function(t){b(t,e.data_src,null)})}},Z=function t(n,e){b(n,e.data_bg,null),b(n,e.data_bg_hidpi,null)},tt=function t(n,e){b(n,e.data_bg_multi,null),b(n,e.data_bg_multi_hidpi,null)},tn=function t(n,e){var a=Y[n.tagName];if(a){a(n,e);return}Z(n,e)},te=["IMG","IFRAME","VIDEO"],ta=function t(n,e){var a,r;e&&!((a=e).loadingCount>0)&&!((r=e).toLoadCount>0)&&N(n.callback_finish,e)},ti=function t(n,e,a){n.addEventListener(e,a),n.llEvLisnrs[e]=a},tr=function t(n,e,a){n.removeEventListener(e,a)},to=function t(n){return!!n.llEvLisnrs},tl=function t(n,e,a){to(n)||(n.llEvLisnrs={});var r="VIDEO"===n.tagName?"loadeddata":"load";ti(n,r,e),ti(n,"error",a)},ts=function t(n){if(to(n)){var e=n.llEvLisnrs;for(var a in e){var r=e[a];tr(n,a,r)}delete n.llEvLisnrs}},tc=function t(n,e,a){A(n),C(a,-1),R(a),L(n,e.class_loading),e.unobserve_completed&&_(n,a)},tu=function t(n,e,a,r){var o=z(e);tc(e,a,r),I(e,a.class_loaded),m(e,"loaded"),tn(e,a),N(a.callback_loaded,e,r),o||ta(a,r)},td=function t(n,e,a,r){var o=z(e);tc(e,a,r),I(e,a.class_error),m(e,d),N(a.callback_error,e,r),o||ta(a,r)},tf=function t(n,e,a){var r=k(n)||n;if(!to(r)){var o=function t(o){tu(o,n,e,a),ts(r)},l=function t(o){td(o,n,e,a),ts(r)};tl(r,o,l)}},t8=function t(n,e,a){$(n),tf(n,e,a),H(n,e,a),J(n,e,a)},tg=function t(n,e,a){tf(n,e,a),K(n,e),X(n,e,a)},tv=function t(n,e,a){var r;(r=n,te.indexOf(r.tagName)>-1)?tg(n,e,a):t8(n,e,a)},tp=function t(n,e,a){tf(n,e,a),K(n,e),tn(n,e),m(n,f)},tb=function t(n,e,a,r){var o;if(a.cancel_on_exit)h(o=n)===u&&"IMG"===n.tagName&&(ts(n),q(n),U(n),L(n,a.class_loading),C(r,-1),y(n),N(a.callback_cancel,n,e,r))},th=function t(n,e,a,r){var o;N(a.callback_enter,n,e,r),O(n,a,r),E(o=n)&&tv(n,a,r)},tm=function t(n,e,a,r){E(n)||(tb(n,e,a,r),N(a.callback_exit,n,e,r))},ty=["IMG","IFRAME"],tE=function t(n){return n.use_native&&"loading"in HTMLImageElement.prototype},tz=function t(n,e,a){n.forEach(function(t){-1!==ty.indexOf(t.tagName)&&(t.setAttribute("loading","lazy"),tp(t,e,a))}),x(a,0)},tN=function t(n,e,a){n.forEach(function(t){var n;return(n=t).isIntersecting||n.intersectionRatio>0?th(t.target,t,e,a):tm(t.target,t,e,a)})},tI=function t(n,e){e.forEach(function(t){n.observe(t)})},tL=function t(n,e){M(n),tI(n,e)},t$=function t(n,e){var r;!(!a||tE(n))&&(e._observer=new IntersectionObserver(function(t){tN(t,n,e)},{root:(r=n).container===document?null:r.container,rootMargin:r.thresholds||r.threshold+"px"}))},tA=function t(n){return Array.prototype.slice.call(n)},tk=function t(n){return n.container.querySelectorAll(n.elements_selector)},t_=function t(n){var e;return h(e=n)===d},tM=function t(n,e){var a;return a=n||tk(e),tA(a).filter(E)},tO=function t(n,e){var a;(a=tk(n),tA(a).filter(t_)).forEach(function(t){L(t,n.class_error),y(t)}),e.update()},tC=function t(e,a){n&&window.addEventListener("online",function(){tO(e,a)})},tR=function t(n,e){var a=s(n);this._settings=a,this.loadingCount=0,t$(a,this),tC(a,this),this.update(e)};return tR.prototype={update:function t(n){var r=this._settings,o=tM(n,r);if(x(this,o.length),e||!a){this.loadAll(o);return}if(tE(r)){tz(o,r,this);return}tL(this._observer,o)},destroy:function t(){this._observer&&this._observer.disconnect(),tk(this._settings).forEach(function(t){delete t.llOriginalAttrs}),delete this._observer,delete this._settings,delete this.loadingCount,delete this.toLoadCount},loadAll:function t(n){var e=this,a=this._settings;tM(n,a).forEach(function(t){tv(t,a,e)})}},tR.load=function(t,n){var e=s(n);tv(t,e)},tR.resetStatus=function(t){y(t)},n&&function t(n,e){if(e){if(e.length)for(var a,r=0;a=e[r];r+=1)c(n,a);else c(n,e)}}(tR,window.lazyLoadOptions),tR});