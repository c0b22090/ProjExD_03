import random
import sys
import time

import pygame as pg


WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ
NUM_OF_BOMBS = 5  #爆弾の数


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数：こうかとん，または，爆弾SurfaceのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


class Bird:
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0),
    }

    def __init__(self, num: int, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 xy：こうかとん画像の位置座標タプル
        """
        self.img = pg.transform.flip(  # 左右反転
            pg.transform.rotozoom(  # 2倍に拡大
                pg.image.load(f"ex03/fig/{num}.png"), 
                0, 
                2.0), 
            True, 
            False
        )
        kk_img = pg.image.load("ex02/fig/3.png")
        kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
        kk_img_f = pg.transform.flip(kk_img, True, False)
        kk_img_1 = pg.transform.rotozoom(kk_img, 315, 1.0)
        kk_img_2 = pg.transform.rotozoom(kk_img, 0, 1.0)
        kk_img_3 = pg.transform.rotozoom(kk_img, 45, 1.0)
        kk_img_4 = pg.transform.rotozoom(kk_img_f, 270, 1.0)
        kk_img_5 = pg.transform.rotozoom(kk_img_f, 315, 1.0)
        kk_img_6 = pg.transform.rotozoom(kk_img_f, 0, 1.0)
        kk_img_7 = pg.transform.rotozoom(kk_img_f, 45, 1.0)
        kk_img_8 = pg.transform.rotozoom(kk_img_f, 90, 1.0)
        self.kk_img_lst = [kk_img_1, kk_img_2, kk_img_3, kk_img_4, kk_img_5, kk_img_6, kk_img_7, kk_img_8]
        self.kk_mv_xy = [[-5, -5], [-5, 0], [-5, +5], [0, +5], [+5, +5], [+5, 0], [+5, -5], [0, -5]]

        self.rct = self.img.get_rect()
        self.rct.center = xy
        self.dire = [+5, 0]

    def change_img(self, num: int, screen: pg.Surface):
        """
        こうかとん画像を切り替え，画面に転送する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 screen：画面Surface
        """
        self.img = pg.transform.rotozoom(pg.image.load(f"ex03/fig/{num}.png"), 0, 2.0)
        screen.blit(self.img, self.rct)

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
                self.dire[0] = sum_mv[0]
                self.dire[1] = sum_mv[1]
        self.rct.move_ip(sum_mv)
        for i in range(8):  #向きごとのこうかとんの表示
            if self.kk_mv_xy[i] == sum_mv:
                self.img = self.kk_img_lst[i]
        if check_bound(self.rct) != (True, True):
            self.rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(self.img, self.rct)


class Bomb:
    """
    爆弾に関するクラス
    """
    def __init__(self, color: tuple[int, int, int], rad: int):
        """
        引数に基づき爆弾円Surfaceを生成する
        引数1 color：爆弾円の色タプル
        引数2 rad：爆弾円の半径
        """
        self.img = pg.Surface((2*rad, 2*rad))
        pg.draw.circle(self.img, color, (rad, rad), rad)
        self.img.set_colorkey((0, 0, 0))
        self.rct = self.img.get_rect()
        self.rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        self.vx, self.vy = +5, +5

    def update(self, screen: pg.Surface):
        """
        爆弾を速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        yoko, tate = check_bound(self.rct)
        if not yoko:
            self.vx *= -1
        if not tate:
            self.vy *= -1
        self.rct.move_ip(self.vx, self.vy)
        screen.blit(self.img, self.rct)


class Beam:
    def __init__(self, bird: Bird):
        self.img = pg.image.load(f"ex03/fig/beam.png")
        self.img_f = pg.transform.flip(self.img, True, False)
        self.img_1 = pg.transform.rotozoom(self.img_f, 315, 1.0)
        self.img_2 = pg.transform.rotozoom(self.img_f, 0, 1.0)
        self.img_3 = pg.transform.rotozoom(self.img_f, 45, 1.0)
        self.img_4 = pg.transform.rotozoom(self.img, 270, 1.0)
        self.img_5 = pg.transform.rotozoom(self.img, 315, 1.0)
        self.img_6 = pg.transform.rotozoom(self.img, 0, 1.0)
        self.img_7 = pg.transform.rotozoom(self.img, 45, 1.0)
        self.img_8 = pg.transform.rotozoom(self.img, 90, 1.0)
        """
        ビームのそれぞれの向きの画像を格納したリスト
        こうかとんの移動方向を格納したリスト
        """
        self.img_lst = [self.img_1, self.img_2, self.img_3, self.img_4, self.img_5, self.img_6, self.img_7, self.img_8]
        self.mv_xy = [[-5, -5], [-5, 0], [-5, +5], [0, +5], [+5, +5], [+5, 0], [+5, -5], [0, -5]]
        self.rct = self.img.get_rect()
        self.vx, self.vy = bird.dire[0], bird.dire[1]
        self.rct.centerx = bird.rct.centerx + bird.rct.width * self.vx / 5
        self.rct.centery = bird.rct.centery + bird.rct.height * self.vy / 5

    def update(self, screen: pg.Surface):
        for i in range(8):  #こうかとんの向きに応じた画像の設定
            if [self.vx, self.vy] == self.mv_xy[i]:
                self.img = self.img_lst[i]
        self.rct.move_ip(self.vx, self.vy)
        screen.blit(self.img, self.rct)


class Effect:
    def __init__(self, bomb: Bomb):
        self.img = pg.image.load(f"ex03/fig/explosion.gif")
        self.img_f = pg.transform.flip(self.img, True, True)
        self.rct = self.img.get_rect()
        self.rct.center = bomb.rct.center
        self.img_lst = [self.img, self.img_f] #切り替わるエフェクトのリスト
        self.life = 10

    def update(self, screen: pg.surface):
        screen.blit(self.img_lst[self.life%2], self.rct)
        self.life -= 1


def main():
    pg.display.set_caption("たたかえ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))    
    bg_img = pg.image.load("ex03/fig/pg_bg.jpg")
    bird = Bird(3, (900, 400))
    bombs = [Bomb((255, 0, 0), 10) for _ in range(NUM_OF_BOMBS)]
    beam = None

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                beam = Beam(bird) #スペースキーを押すとビームが表示
        
        screen.blit(bg_img, [0, 0])
        
        for bomb in bombs:
            if bird.rct.colliderect(bomb.rct):
                # ゲームオーバー時に，こうかとん画像を切り替え，1秒間表示させる
                bird.change_img(8, screen)
                pg.display.update()
                time.sleep(1)
                return
        
        for i, bomb in enumerate(bombs):
            effects = [Effect(bombs[i]) for _ in range(NUM_OF_BOMBS)]
            if beam is not None:
                if beam.rct.colliderect(bomb.rct): #爆弾にビームが当たったとき
                    if effects[i].life == 0:
                        effects[i] = None
                    beam = None
                    bombs[i] = None
                    bird.change_img(6, screen)
                    pg.display.update()
                    effects = [effect for effect in effects if effect is not None]
                    for effect in effects: #エフェクトの表示
                        effect.update(screen)

        key_lst = pg.key.get_pressed()
        bird.update(key_lst, screen)
        bombs = [bomb for bomb in bombs if bomb is not None]
        for bomb in bombs:
            bomb.update(screen)

        if beam is not None:
            beam.update(screen)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()