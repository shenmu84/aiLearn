class InkSystem {
  constructor() {
    this.canvas = document.getElementById('inkCanvas');
    this.ctx = this.canvas.getContext('2d');
    this.fish = [];
    this.init();
  }

  init() {
    this.resizeHandler();
    window.addEventListener('resize', this.resizeHandler.bind(this));

    // 初始化三条金鱼
    for(let i = 0; i < 3; i++) {
      this.fish.push(new GoldenFish(
        Math.random() * this.canvas.width,
        Math.random() * this.canvas.height
      ));
    }

    this.animate();
  }

  resizeHandler() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }

  animate() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // 绘制山水背景
    this.drawMountain();

    // 更新金鱼位置
    this.fish.forEach(fish => {
      fish.update();
      fish.draw(this.ctx);
    });

    requestAnimationFrame(this.animate.bind(this));
  }

  drawMountain() {
    // 山水绘制算法
    const grad = this.ctx.createLinearGradient(0, 0, 0, this.canvas.height);
    grad.addColorStop(0, 'rgba(45,45,45,0.1)');
    grad.addColorStop(1, 'rgba(157,31,31,0.08)');

    this.ctx.beginPath();
    // ...山水路径绘制代码
    this.ctx.fillStyle = grad;
    this.ctx.fill();
  }
}

class GoldenFish {
  constructor(x, y) {
    this.path = this.generatePath();
    this.progress = 0;
  }

  generatePath() {
    // 生成贝塞尔曲线路径
    return {
      start: {x: -100, y: Math.random()*window.innerHeight},
      cp1: {x: window.innerWidth*0.3, y: Math.random()*window.innerHeight},
      cp2: {x: window.innerWidth*0.7, y: Math.random()*window.innerHeight},
      end: {x: window.innerWidth+100, y: Math.random()*window.innerHeight}
    };
  }

  update() {
    this.progress += 0.002;
    if(this.progress >= 1) {
      this.path = this.generatePath();
      this.progress = 0;
    }
  }

  draw(ctx) {
    // 金鱼绘制逻辑
    const pos = this.calculatePosition();

    ctx.save();
    ctx.translate(pos.x, pos.y);
    ctx.rotate(Math.atan2(pos.dy, pos.dx));

    // 绘制金鱼身体
    ctx.beginPath();
    ctx.fillStyle = 'rgba(157,31,31,0.9)';
    // ...金鱼形状路径
    ctx.fill();

    // 绘制烫金鱼鳞
    ctx.beginPath();
    ctx.fillStyle = 'rgba(212,175,55,0.6)';
    // ...鳞片绘制代码
    ctx.fill();

    ctx.restore();
  }
}