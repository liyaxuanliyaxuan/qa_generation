## 力学(上册)

### (1) $t = \frac{1}{3}T$ 时的位置、速度和加速度；
### (2) 在 $t = 0$ 至 $t = \frac{1}{3}T$ 期间，质点的位置、平均速度和平均加速度。

解 (1) 由轨道方程可知，质点做圆周运动。再由 $t = 0$ 时从原点出发，以恒定速率向 $x$ 正方向运动。可直接写出质点的运动学方程为

$$
x = r \sin \omega t
$$

$$
y = r (1 - \cos \omega t)
$$

其中 $\omega$ 为常量。

运动学方程也可用解微分方程得到，方法如下：

$$
y = r - \sqrt{r^2 - x^2}
$$

(考虑到 $t = 0$ 时，$x = 0$, $y = 0$, 取负号)

$$
\dot{y} = + \frac{x}{\sqrt{r^2 - x^2}} \dot{x}
$$

$$
\dot{x}^2 + \dot{y}^2 = \dot{x}^2 + \frac{x^2}{r^2 - x^2} \dot{x}^2 = \frac{r^2 \dot{x}^2}{r^2 - x^2} = v^2
$$

这里 $v$ 为速率，是常量。

由于 $T = \frac{2 \pi r}{v}$, 且 $v > 0$, 所以

$$
r \frac{dx}{dt} = v \sqrt{r^2 - x^2}
$$

(开方并取正号)

$$
\int_0^x \frac{r dx}{\sqrt{r^2 - x^2}} = \int_0^t v dt
$$

$$
x = r \sin \left( \frac{v}{r} t \right)
$$

$$
y = r - r \cos \left( \frac{v}{r} t \right) = r \left[ 1 - \cos \left( \frac{v}{r} t \right) \right]
$$

由 $t = T$ 时 $x = 0$, $y = 0$, 可得

$$
x = r \sin \left( \frac{2 \pi}{T} t \right)
$$

$$
y = r \left[ 1 - \cos \left( \frac{2 \pi}{T} t \right) \right]
$$

$t = \frac{1}{3} T$ 时，

$$
x = r \sin \frac{2 \pi}{3} = \frac{\sqrt{3}}{2} r
$$

$$
y = r \left[ 1 - \cos \frac{2 \pi}{3} \right] = \frac{3}{2} r
$$

$$
r \left| \frac{T}{3} \right| = \frac{\sqrt{3}}{2} r \mathbf{i} + \frac{3}{2} r \mathbf{j}
$$

$$
r(t) = r \sin \left( \frac{2 \pi}{T} t \right) \mathbf{i} + r \left[ 1 - \cos \left( \frac{2 \pi}{T} t \right) \right] \mathbf{j}
$$

