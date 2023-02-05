const canvas = document.querySelector("canvas");
const c = canvas.getContext("2d");

const scoreEl = document.querySelector("#scoreEl");
const modalScoreEl = document.querySelector("#modalScoreEl");
const modalEl = document.querySelector("#modalEl");
const buttonEl = document.querySelector("#buttonEl");
const startButtonEl = document.querySelector("#startButtonEl");
const startModalEl = document.querySelector("#startModalEl");

canvas.width = innerWidth;
canvas.height = innerHeight;

class Player {
	constructor(x, y, radius, color) {
		this.x = x;
		this.y = y;
		this.radius = radius;
		this.color = color;
		this.velocity = {
			x: 0,
			y: 0,
		};
	}

	draw() {
		c.beginPath();
		c.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
		c.fillStyle = this.color;
		c.fill();
	}

	update() {
		this.draw();

		const friction = 0.99;

		this.velocity.x *= friction;
		this.velocity.y *= friction;
		if (
			this.x + this.radius + this.velocity.x <= canvas.width &&
			this.x - this.radius + this.velocity.x >= 0
		) {
			this.x += this.velocity.x;
		} else {
			this.velocity.x = 0;
		}

		if (
			this.y + this.radius + this.velocity.y <= canvas.height &&
			this.y - this.radius + this.velocity.y >= 0
		) {
			this.y += this.velocity.y;
		} else {
			this.velocity.y = 0;
		}
	}
}

class Projectile {
	constructor(x, y, radius, color, velocity) {
		this.x = x;
		this.y = y;
		this.radius = radius;
		this.color = color;
		this.velocity = velocity;
	}

	draw() {
		c.beginPath();
		c.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
		c.fillStyle = this.color;
		c.fill();
	}

	update() {
		this.draw();
		this.x += this.velocity.x;
		this.y += this.velocity.y;
	}
}

class Enemy {
	constructor(x, y, radius, color, velocity) {
		this.x = x;
		this.y = y;
		this.radius = radius;
		this.color = color;
		this.velocity = velocity;
		this.type = "Linear";
		this.radians = 0;

		this.center = {
			x,
			y,
		}

		if (Math.random() < 0.5 ) {
			this.type = 'Homing'
			if (Math.random() < 0.5 ) {
				this.type = 'Spinning'
			}
		}
	}

	draw() {
		c.beginPath();
		c.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
		c.fillStyle = this.color;
		c.fill();
	}

	update() {
		this.draw();

		// if (this.type === 'Homing') {
		// 	const radian = Math.atan2(player.y - this.y, player.x - this.x);
		// 	this.velocity.x = Math.cos(radian);
		// 	this.velocity.y = Math.sin(radian);
		// }
		// this.x += this.velocity.x;
		// this.y += this.velocity.y;

		if(this.type ==='Spinning'){
			this.radians += 0.1;

			this.center.x += this.velocity.x;
			this.center.y += this.velocity.y;

			this.x = this.center.x  + Math.cos(this.radians) * 30;
			this.y = this.center.x  + Math.sin(this.radians) * 30;

		} else if (this.type === 'Homing'){
			const radian = Math.atan2(player.y - this.y, player.x - this.x);
			this.velocity.x = Math.cos(radian);
			this.velocity.y = Math.sin(radian);
			this.x += this.velocity.x;
			this.y += this.velocity.y;
		} else {
			this.x += this.velocity.x;
			this.y += this.velocity.y;
		}

	}
}

const friction = 0.99;
class Particle {
	constructor(x, y, radius, color, velocity) {
		this.x = x;
		this.y = y;
		this.radius = radius;
		this.color = color;
		this.velocity = velocity;
		this.alpha = 1;
	}

	draw() {
		c.save();
		c.globalAlpha = 0.1;
		c.beginPath();
		c.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
		c.fillStyle = this.color;
		c.fill();
		c.restore();
	}

	update() {
		this.draw();
		this.alpha -= 0.01;
		this.velocity.x *= friction;
		this.velocity.y *= friction;
		this.x += this.velocity.x;
		this.y += this.velocity.y;
	}
}

const x = canvas.width / 2;
const y = canvas.height / 2;

let player = new Player(x, y, 10, "white");
let projectiles = [];
let enemies = [];
let particles = [];
let animationId;
let intervalId;
let score = 0;

function init() {
	player = new Player(x, y, 10, "white");
	projectiles = [];
	enemies = [];
	particles = [];
	animationId;
	score = 0;
}

function spawnEnemies() {
	intervalId = setInterval(() => {
		const radius = Math.random() * (30 - 4) + 4;
		let x;
		let y;
		// 在左右两列生成 x 固定左 右 y随机
		if (Math.random() < 0.5) {
			x = Math.random() < 0.5 ? 0 - radius : canvas.width + radius;
			y = Math.random() * canvas.height;

			// 在上下两列生成 y 固定上下 x随机
		} else {
			x = Math.random() * canvas.width;
			y = Math.random() < 0.5 ? 0 - radius : canvas.height + radius;
		}
		// const x = Math.random() < 0.5 ? 0 - radius : canvas.width + radius
		// const y = Math.random() < 0.5 ? 0 - radius : canvas.height + radius
		const color = `hsl(${Math.random() * 360}, 50%, 50%)`;

		const radian = Math.atan2(canvas.height / 2 - y, canvas.width / 2 - x);

		const velocity = {
			x: Math.cos(radian),
			y: Math.sin(radian),
		};

		enemies.push(new Enemy(x, y, radius, color, velocity));
	}, 1000);
}

function animate() {
	animationId = requestAnimationFrame(animate);
	// 透明度叠加 会形成特效 淡入淡出效果
	c.fillStyle = "rgba(0, 0, 0, 0.1)";
	c.fillRect(0, 0, canvas.width, canvas.height);

	// player.draw();
	player.update();

	for (let p_i = particles.length - 1; p_i >= 0; p_i--) {
		p = particles[p_i];
		p.update();
		if (p.alpha <= 0) {
			// setTimeout(() => {
			particles.splice(p_i, 1);
			// });
		}
	}

	for (let p_i = projectiles.length - 1; p_i >= 0; p_i--) {
		p = projectiles[p_i];
		p.update();

		// 越界
		if (
			p.x - p.radius < 0 ||
			p.x + p.radius > canvas.width ||
			p.y - p.radius < 0 ||
			p.y + p.radius > canvas.height
		) {
			// setTimeout(() => {
			projectiles.splice(p_i, 1);
			// });
		}
	}

	// 这里和初始使用 foreach 的一些区别, foreach 如果用 splice 移除的时候
	// 下一帧渲染的话, 元素可能就不大对,
	// 所以使用倒序的方式, 这样前面元素的渲染就不会出问题.
	for (let e_i = enemies.length - 1; e_i >= 0; e_i--) {
		e = enemies[e_i];

		e.update();

		const dist = Math.hypot(player.x - e.x, player.y - e.y);

		// 玩家碰撞
		if (dist - e.radius - player.radius < 1) {
			cancelAnimationFrame(animationId);
			clearInterval(intervalId);

			modalEl.style.display = "block";
			modalScoreEl.innerHTML = score;

			gsap.fromTo(
				"#modalEl",
				{
					scale: 0.8,
					opacity: 0,
				},
				{
					scale: 1,
					opacity: 1,
					ease: "expo.in",
				}
			);
		}

		// 子弹碰撞
		for (let p_i = projectiles.length - 1; p_i >= 0; p_i--) {
			p = projectiles[p_i];

			const dist = Math.hypot(p.x - e.x, p.y - e.y);

			if (dist - e.radius - p.radius < 1) {
				for (let i = 0; i < e.radius * 2; i++) {
					particles.push(
						new Particle(p.x, p.y, Math.random() * 2, e.color, {
							x: (Math.random() - 0.5) * (Math.random() * 6),
							y: (Math.random() - 0.5) * (Math.random() * 6),
						})
					);
				}
				// 过滤掉大于 10
				if (e.radius - 10 > 5) {
					score += 50;
					scoreEl.innerHTML = score;
					// e.radius -= 10;
					gsap.to(e, {
						radius: e.radius - 10,
					});
					// setTimeout(() => {
					projectiles.splice(p_i, 1);
					// });
				} else {
					score += 100;
					scoreEl.innerHTML = score;
					// 使用倒序时候就不需要用 setTimeout 了, 不会宥闪烁
					// setTimeout(() => {
					enemies.splice(e_i, 1);
					projectiles.splice(p_i, 1);
					// });
				}
			}
		}
	}
}

addEventListener("click", (event) => {
	const radian = Math.atan2(
		event.clientY - player.y,
		event.clientX - player.x
	);

	const velocity = {
		x: Math.cos(radian) * 4,
		y: Math.sin(radian) * 4,
	};

	projectiles.push(new Projectile(player.x, player.y, 5, "white", velocity));
});

buttonEl.addEventListener("click", () => {
	init();
	animate();
	spawnEnemies();
	// modalEl.style.display = "none";

	gsap.to("#modalEl", {
		opacity: 0,
		scale: 0.8,
		duration: 0.2,
		ease: "expo.in",
		onComplete: () => {
			modalEl.style.display = "none";
		},
	});
});

// gasp visualization;
startButtonEl.addEventListener("click", () => {
	init();
	animate();
	spawnEnemies();
	// startModalEl.style.display = "none";
	gsap.to("#startModalEl", {
		opacity: 0,
		scale: 0.8,
		duration: 0.2,
		ease: "expo.in",
		onComplete: () => {
			startModalEl.style.display = "none";
		},
	});
});

window.addEventListener("keydown", (event) => {
	switch (event.key) {
		case "a":
			player.velocity.x -= 1;
			break;
		case "d":
			player.velocity.x += 1;
			break;
		case "w":
			player.velocity.y -= 1;
			break;
		case "s":
			player.velocity.y += 1;
			break;
	}
});
