import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class MirrorParams:
    x_pos: float
    y_pos: float
    z_pos: float
    angle_xy: float
    angle_z: float
    incident_angle_xy: float
    incident_angle_z: float

class ReflectionSimulator:
    def __init__(self):
        self.mirror_params = []
        
    def calculate_reflection_3d(self, incident_point, incident_angle_xy, incident_angle_z, 
                              mirror_angle_xy=0, mirror_angle_z=0, ray_length=2):
        incident_xy_rad = np.radians(incident_angle_xy)
        incident_z_rad = np.radians(incident_angle_z)
        mirror_xy_rad = np.radians(mirror_angle_xy)
        mirror_z_rad = np.radians(mirror_angle_z)
        
        incident = np.array([
            np.cos(incident_z_rad) * np.cos(incident_xy_rad),
            np.cos(incident_z_rad) * np.sin(incident_xy_rad),
            np.sin(incident_z_rad)
        ])
        
        normal = np.array([
            np.sin(mirror_xy_rad) * np.cos(mirror_z_rad),
            -np.cos(mirror_xy_rad) * np.cos(mirror_z_rad),
            np.sin(mirror_z_rad)
        ])
        normal = normal / np.linalg.norm(normal)
        
        reflection = incident - 2 * np.dot(incident, normal) * normal
        
        incident_end = np.array(incident_point) + ray_length * incident
        reflected_end = np.array(incident_point) + ray_length * reflection
        
        return incident_end, reflected_end

    def create_mirror_controls(self, mirror_index):
        with st.sidebar:
            st.subheader(f"Miroir {mirror_index+1}")
            
            params = {}
            for param in ['x', 'y', 'z']:
                col1, col2 = st.columns(2)
                with col1:
                    slider = st.slider(f"{param.upper()} - M{mirror_index+1}", -5.0, 5.0, 0.0, 0.1)
                with col2:
                    params[f"{param}_pos"] = st.number_input(
                        f"{param.upper()} exact - M{mirror_index+1}", -5.0, 5.0, slider, 0.1
                    )
            
            for angle_type in ['xy', 'z']:
                name = "XY" if angle_type == "xy" else "Élévation"
                col1, col2 = st.columns(2)
                with col1:
                    slider = st.slider(f"Angle {name} M{mirror_index+1}", -90, 90, 0)
                with col2:
                    params[f"angle_{angle_type}"] = st.number_input(
                        f"Angle {name} exact M{mirror_index+1}", -90, 90, slider
                    )
            
            for inc_type in ['xy', 'z']:
                name = "XY" if inc_type == "xy" else "Z"
                range_val = (-180, 180) if inc_type == "xy" else (-90, 90)
                default = 45 if inc_type == "xy" else 0
                
                col1, col2 = st.columns(2)
                with col1:
                    slider = st.slider(f"Incidence {name} M{mirror_index+1}", *range_val, default)
                with col2:
                    params[f"incident_angle_{inc_type}"] = st.number_input(
                        f"Incidence {name} exact M{mirror_index+1}", *range_val, slider
                    )
            
            return MirrorParams(**params)

    def plot_normal_3d(self, ax, incident_point, mirror_angle_xy, mirror_angle_z, view='top'):
        normal_length = 0.5
        if view == 'top':
            normal_angle = np.radians(mirror_angle_xy + 90)
            normal_x = [incident_point[0], incident_point[0] + normal_length * np.cos(normal_angle)]
            normal_y = [incident_point[1], incident_point[1] + normal_length * np.sin(normal_angle)]
            ax.plot(normal_x, normal_y, 'g:', linewidth=1)
        else:
            normal_angle = np.radians(mirror_angle_z + 90)
            normal_x = [incident_point[0], incident_point[0] + normal_length * np.cos(normal_angle)]
            normal_z = [incident_point[2], incident_point[2] + normal_length * np.sin(normal_angle)]
            ax.plot(normal_x, normal_z, 'g:', linewidth=1)

    def plot_mirror_3d(self, ax1, ax2, params):
        incident_point = (params.x_pos, params.y_pos, params.z_pos)
        incident_end, reflected_end = self.calculate_reflection_3d(
            incident_point,
            params.incident_angle_xy,
            params.incident_angle_z,
            params.angle_xy,
            params.angle_z
        )
        
        self._plot_rays(ax1, incident_point, incident_end, reflected_end, plane='xy')
        self._plot_rays(ax2, incident_point, incident_end, reflected_end, plane='xz')
        
        # Passage du paramètre plane pour chaque vue
        self._plot_mirror(ax1, incident_point, params.angle_xy, plane='xy')
        self._plot_mirror(ax2, (incident_point[0], 0, incident_point[2]), params.angle_z, plane='xz')
        
        self.plot_normal_3d(ax1, incident_point, params.angle_xy, params.angle_z, 'top')
        self.plot_normal_3d(ax2, (incident_point[0], 0, incident_point[2]), 
                        params.angle_xy, params.angle_z, 'side')

    def _plot_rays(self, ax, incident_point, incident_end, reflected_end, plane='xy'):
        idx1, idx2 = (0, 1) if plane == 'xy' else (0, 2)
        
        if 'Rayon incident' not in [line.get_label() for line in ax.get_lines()]:
            ax.plot([incident_end[idx1], incident_point[idx1]], 
                   [incident_end[idx2], incident_point[idx2]], 
                   'b-', label='Rayon incident')
            ax.plot([incident_point[idx1], reflected_end[idx1]], 
                   [incident_point[idx2], reflected_end[idx2]], 
                   'r--', label='Rayon réfléchi')
        else:
            ax.plot([incident_end[idx1], incident_point[idx1]], 
                   [incident_end[idx2], incident_point[idx2]], 'b-')
            ax.plot([incident_point[idx1], reflected_end[idx1]], 
                   [incident_point[idx2], reflected_end[idx2]], 'r--')

    def _plot_mirror(self, ax, point, angle, plane='xy'):
        mirror_length = 1
        mirror_rad = np.radians(angle)
        
        if plane == 'xy':
            # Vue du dessus (plan XY)
            mirror_x = [point[0] - mirror_length * np.cos(mirror_rad),
                    point[0] + mirror_length * np.cos(mirror_rad)]
            mirror_y = [point[1] - mirror_length * np.sin(mirror_rad),
                    point[1] + mirror_length * np.sin(mirror_rad)]
        else:
            # Vue de côté (plan XZ)
            mirror_x = [point[0] - mirror_length * np.cos(mirror_rad),
                    point[0] + mirror_length * np.cos(mirror_rad)]
            mirror_y = [point[2] - mirror_length * np.sin(mirror_rad),
                    point[2] + mirror_length * np.sin(mirror_rad)]
        
        ax.plot(mirror_x, mirror_y, 'k-', linewidth=2)

    def setup_axes(self, ax1, ax2):
        for ax, title in [(ax1, 'Vue du dessus (plan XY)'), (ax2, 'Vue de côté (plan XZ)')]:
            ax.set_xlim(-6, 6)
            ax.set_ylim(-6, 6)
            ax.grid(True)
            ax.set_aspect('equal')
            ax.set_xlabel('X')
            ax.set_ylabel('Y' if ax == ax1 else 'Z')
            ax.set_title(title)
            
            handles, labels = ax.get_legend_handles_labels()
            by_label = dict(zip(labels, handles))
            ax.legend(by_label.values(), by_label.keys())

    def display_parameters(self, mirror_params):
        st.write("### Paramètres des miroirs")
        for i, params in enumerate(mirror_params):
            st.write(f"### Miroir {i+1}")
            st.write(f"- Position: ({params.x_pos:.1f}, {params.y_pos:.1f}, {params.z_pos:.1f})")
            st.write(f"- Angle XY: {params.angle_xy}°")
            st.write(f"- Élévation: {params.angle_z}°")
            st.write(f"- Angle d'incidence XY: {params.incident_angle_xy}°")
            st.write(f"- Angle d'incidence Z: {params.incident_angle_z}°")

    def run(self):
        st.title("Simulateur de Réflexion 3D")
        
        with st.sidebar:
            st.header("Configuration")
            col1, col2 = st.columns(2)
            with col1:
                num_mirrors = st.slider("Nombre de miroirs", 1, 4, 2)
            with col2:
                num_mirrors = st.number_input("Nombre exact", 1, 4, 2)
        
        self.mirror_params = [self.create_mirror_controls(i) for i in range(num_mirrors)]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
        
        for params in self.mirror_params:
            self.plot_mirror_3d(ax1, ax2, params)
        
        self.setup_axes(ax1, ax2)
        
        st.pyplot(fig)
        
        self.display_parameters(self.mirror_params)