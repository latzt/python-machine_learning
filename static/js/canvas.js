const canvas = document.querySelector('#canvas');
// could be 3d, if you want to make a video game
const ctx = canvas.getContext('2d');
// canvas.width = window.innerWidth;
// canvas.height = window.innerHeight;
ctx.lineJoin = 'round';
ctx.lineCap = 'round';
ctx.lineWidth = 4;
ctx.strokeStyle = '#000000';
ctx.fillStyle = '#ffffff';
ctx.fillRect(0, 0, canvas.width, canvas.height);

let isDrawing = false;
let lastX = 0;
let lastY = 0;

const draw = (e) => {
    if (!isDrawing) {
        return;
    }
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.stroke();
    [lastX, lastY] = [e.offsetX, e.offsetY];
}

const init = () => {
    canvas.addEventListener('mousedown', (e) => {
        isDrawing = true;
        [lastX, lastY] = [e.offsetX, e.offsetY];
    });

    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', () => isDrawing = false);
    canvas.addEventListener('mouseout', () => isDrawing = false);
}

const erase = () => {
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

const toBlob = (callback, type) => {
    return canvas.toBlob(callback, type);
}

const toDataURL = (mime) => {
    return canvas.toDataURL(mime);
}

export { init, erase, toBlob, toDataURL };