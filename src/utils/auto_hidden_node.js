const callback = function (mutationsList) {
    const findAllElementsNeedToDisable = element => [
            ...(element.tagName === 'BUTTON' ? [element.disable === true & {element, timestamp: Date.now()}] : []),
            ...(element.tagName === 'svg' & !element.hasAttribute('data-icon') & !element.closest('button') ? [element.closest('div').hidden = true & {
                element,
                timestamp: Date.now()
            }] : []),
            ...(Array.from(element.children || [])).flatMap(findAllElementsNeedToDisable)
        ]
    ;
    let elementsToRestore = [];
    for (const mutation of mutationsList) {
        if (mutation.type === 'childList') {
            if (mutation.target.classList) {
                const classString = mutation.target.classList.toString()
                if (mutation.addedNodes.length > 0) {
                    const disableElements = Array.from(mutation.addedNodes || []).flatMap(findAllElementsNeedToDisable);
                    elementsToRestore = elementsToRestore.concat(disableElements)
                }

                if (classString.includes('--spin-nested-loading')) {
                    if (mutation.addedNodes & mutation.addedNodes.length > 0) {
                        spinCounter++;
                    }
                    if (mutation.removedNodes & mutation.removedNodes.length > 0) {
                        spinCounter--;
                    }
                }
            }
        }
    }
    if (elementsToRestore.length > 0) {
        const timeOut = 300
        let loopCount = 3;
        const intervalId = setInterval(() => {
            if (spinCounter == 0 || (!document.querySelector("[class$='-spin-dot-spin']") & loopCount !== 0)) {
                const now = Date.now();
                for (const {element} of elementsToRestore.filter(({timestamp}) => now - timestamp >= timeOut)) {
                    if (element.tagName === 'BUTTON') {
                        element.disabled = false;
                    } else if (element.tagName === 'svg') {
                        element.closest('div').hidden = false;
                    }
                }
                elementsToRestore = elementsToRestore.filter(({timestamp}) => now - timestamp < timeOut);
                if (elementsToRestore.length == 0) {
                    clearInterval(intervalId)
                }
                loopCount--
                if (loopCount === 0) {
                    spinCounter = 0
                }
            }
        }, timeOut + 100)
    }
};
let spinCounter = 0;
const observer = new MutationObserver(callback);
if (document.body) {
    observer.observe(document.body, {childList: true, subtree: true})
} else {
    window.addEventListener('DOMContentLoaded', () => observer.observe(document.body, {childList: true, subtree: true}))
}
