def check_collision(object, player):

    if player.colliderect(object):
        return True
    else:
        return False
