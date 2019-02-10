import numpy as np
from scipy.spatial import distance
from Vector import Vector


class Orientation:

    def __init__(self):
        # x,y-coordinates from click (to trace movement of pressed mouse)
        self.click_pos = np.array([0, 0])  # former: click_x_y
        self.move_pos = np.array([0, 0])  # if you need the difference of new moved position (vector)
        self.vec_movement = self.move_pos - self.click_pos

        self.angle = 0  # angle between vectors in rad

        self.trace_movement = np.array([0, 0])  # difference of original position since beginning (traces movement)

        # variables for zoom
        self.zoom = 0
        self.zoom_factor = 0.05
        self.trace_zoom = 1
        self.original_current_cv = None
        self.point_of_zoom = None
        self.g = Vector(0, 9.81, 0)  # the gravity acceleration

    def get_click(self):
        # coordinates of a mouse click
        return self.click_pos

    def get_move(self):
        # new coordinates of a moved mouse
        return self.move_pos

    def get_movement(self):
        # difference of new moved and prior coordinates
        self.vec_movement = self.move_pos - self.click_pos
        return self.vec_movement

    def get_trace_movement(self):
        return self.trace_movement

    def get_trace_zoom(self):
        return self.trace_zoom

    def set_click(self, event):
        self.click_pos = np.array([event.pos().x(), event.pos().y()])

    def set_move(self, event):
        self.move_pos = np.array([event.pos().x(), event.pos().y()])

    def set_zoom_settings(self, event):
        self.point_of_zoom = np.array([event.pos().x(), event.pos().y()])
        self.zoom += event.angleDelta().y()//120

    def set_trace_zoom_in(self):
        self.trace_zoom *= (1 + self.zoom_factor)
        self.g *= (1 + self.zoom_factor)

    def set_trace_zoom_out(self):
        self.trace_zoom /= (1 + self.zoom_factor)
        self.g /= (1 + self.zoom_factor)

    def set_trace_movement_while_zoom_in(self):
        self.trace_movement = self.point_of_zoom + ((self.trace_movement - self.point_of_zoom) * (1 + self.zoom_factor))

    def set_trace_movement_while_zoom_out(self):
        self.trace_movement = self.point_of_zoom + ((self.trace_movement - self.point_of_zoom) / (1 + self.zoom_factor))

    def actualize_player_location(self, player):
        pass

    def actualize_click(self):
        self.click_pos = self.move_pos

    def check_click_on_point(self, path, point):
        return (self.click_pos <= point + path.cv_size).all() and (self.click_pos >= point - path.cv_size).all()

    def move_points_and_screen(self, all_paths, player):
        self.trace_movement += self.move_pos - self.click_pos
        for i in range(len(all_paths)):
            all_paths[i] += self.get_movement()  # if it exist, change pos of all cv_paths
        if player is not None:
            player.x, player.y = np.array([player.x, player.y]) + self.get_movement()
        self.click_pos = self.move_pos

    def reset_movement(self):
        self.trace_movement -= self.trace_movement

    def move_to_center(self, all_paths):
        for i in range(len(all_paths)):
            all_paths[i] -= self.trace_movement

        self.trace_movement -= self.trace_movement

        if self.trace_zoom > 1:
            for i in range(len(all_paths)):
                for j in range(len(all_paths[i])):
                    all_paths[i][j] = all_paths[i][j] / self.trace_zoom
            self.trace_zoom /= self.trace_zoom
            self.g /= self.g.y
        else:
            for i in range(len(all_paths)):
                for j in range(len(all_paths[i])):
                    all_paths[i][j] = all_paths[i][j] / self.trace_zoom
            self.trace_zoom /= self.trace_zoom
            self.g /= self.g.y

    def calculate_angle(self, vector_one, vector_two):
        # calculates angle in rad
        ang1 = np.arctan2(*vector_one)
        ang2 = np.arctan2(*vector_two)
        self.angle = (ang2-ang1) % (2*np.pi)

    def calculate_bbox_coordinates(self, active_path, moved_point):
        # TODO: HÄSSLICH! Geht auch mit Matrizenmultiplikation, funktioniert aber noch nicht ganz
        bbox = active_path.bounding_box

        box_center = (bbox[0] + bbox[2])/2
        box_point = bbox[moved_point]
        related_point = bbox[moved_point-1]  # for other points to move too
        norm_length = distance.euclidean(box_center, related_point)
        length = distance.euclidean(self.move_pos, box_center)

        relative_length = length/norm_length

        vector_one = self.move_pos-box_center
        vector_two = box_point-box_center
        self.calculate_angle(vector_two, vector_one)

        punkt_v2 = active_path.cvs - box_center
        # would work point for two matrices
        punkte_laenge_v2 = []
        for i in range(len(active_path.cvs)):
            punkte_laenge_v2.append(distance.euclidean(active_path.cvs[i], box_center))
        for i in range(len(active_path.bounding_box)):
            punkte_laenge_v2.append(distance.euclidean(active_path.bounding_box[i], box_center))
        # evtl. umrechnen in Matrix und dann ein 2-Zeiler?
        # Berechnung der Länge muss auch über Matrix gehen

        for i, each in enumerate(active_path.cvs):

            punkt = active_path.cvs[i] - box_center
            punkt_laenge = distance.euclidean(active_path.cvs[i], box_center)
            punkt = punkt/punkt_laenge

            x, y = punkt

            xx = x * np.cos(self.angle) + y * np.sin(self.angle)
            yy = -x * np.sin(self.angle) + y * np.cos(self.angle)

            active_path.cvs[i] = box_center + (np.array([xx, yy]) * punkt_laenge * relative_length)

        for i, each in enumerate(active_path.bounding_box):
            punkt = active_path.bounding_box[i] - box_center
            punkt_laenge = distance.euclidean(active_path.bounding_box[i], box_center)
            punkt = punkt/punkt_laenge

            x, y = punkt

            xx = x * np.cos(self.angle) + y * np.sin(self.angle)
            yy = -x * np.sin(self.angle) + y * np.cos(self.angle)

            active_path.bounding_box[i] = box_center + (np.array([xx, yy]) * punkt_laenge * relative_length)

        self.click_pos = self.move_pos

    def calculate_zoom_translation(self, cv_list, zoom_in=True):
        """ calculates zoom (in or out) for a list of points """
        for i in range(len(cv_list)):
            if zoom_in:
                cv_list[i] = self.point_of_zoom + (cv_list[i] - self.point_of_zoom) * (1 + self.zoom_factor)
            else:
                cv_list[i] = self.point_of_zoom + (cv_list[i] - self.point_of_zoom) / (1 + self.zoom_factor)

    def calculate_zoom_translation_player(self, player, zoom_in=True):
        """ calculates zoom (in or out) for a player if there's one """
        if player is not None:
            if zoom_in:
                player.x, player.y = self.point_of_zoom + (np.array([player.x, player.y]) - self.point_of_zoom) * (1 + self.zoom_factor)
                player.vector *= (1 + self.zoom_factor)
            else:
                player.x, player.y = self.point_of_zoom + (np.array([player.x, player.y]) - self.point_of_zoom) / (1 + self.zoom_factor)
                player.vector /= (1 + self.zoom_factor)
