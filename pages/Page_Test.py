import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def calculate_reflection(incident_point, incident_angle, mirror_angle=0, ray_length=2):
    incident_rad = np.radians(incident_angle)
    mirror_rad = np.radians(mirror_angle)
    x_incident = incident_point[0] + ray_length * np.cos(incident_rad)
    y_incident = incident_point[1] + ray_length * np.sin(incident_rad)
    normal = np.array([np.sin(mirror_rad), -np.cos(mirror_rad)])
    incident = np.array([np.cos(incident_rad), np.sin(incident_rad)])
    reflection = incident - 2 * np.dot(incident, normal) * normal
    x_reflected = incident_point[0] + ray_length * reflection[0]
    y_reflected = incident_point[1] + ray_length * reflection[1]
    return (x_incident, y_incident), (x_reflected, y_reflected)

st.title("Advanced Reflection Simulator")

with st.sidebar:
    st.header("Configuration")
    col1, col2 = st.columns(2)
    with col1:
        num_mirrors = st.slider("Nombre de miroirs", 1, 4, 2)
    with col2:
        num_mirrors = st.number_input("Nombre exact", 1, 4, 2)

def create_mirror_controls(mirror_index):
    with st.sidebar:
        st.subheader(f"Miroir {mirror_index+1}")
        
        # Position X
        col1, col2 = st.columns(2)
        with col1:
            x_slider = st.slider(f"X - M{mirror_index+1}", -5.0, 5.0, 0.0, 0.1)
        with col2:
            x_input = st.number_input(f"X exact - M{mirror_index+1}", -5.0, 5.0, x_slider, 0.1)
        
        # Position Y
        col1, col2 = st.columns(2)
        with col1:
            y_slider = st.slider(f"Y - M{mirror_index+1}", -5.0, 5.0, 0.0, 0.1)
        with col2:
            y_input = st.number_input(f"Y exact - M{mirror_index+1}", -5.0, 5.0, y_slider, 0.1)
        
        # Mirror Angle
        col1, col2 = st.columns(2)
        with col1:
            angle_slider = st.slider(f"Angle M{mirror_index+1}", -90, 90, 0)
        with col2:
            angle_input = st.number_input(f"Angle exact M{mirror_index+1}", -90, 90, angle_slider)
        
        # Incident Angle
        col1, col2 = st.columns(2)
        with col1:
            incident_slider = st.slider(f"Incidence M{mirror_index+1}", -180, 180, 45)
        with col2:
            incident_input = st.number_input(f"Incidence exact M{mirror_index+1}", -180, 180, incident_slider)
        
        return {
            'x_pos': x_input,
            'y_pos': y_input,
            'angle': angle_input,
            'incident_angle': incident_input
        }

mirror_params = [create_mirror_controls(i) for i in range(num_mirrors)]

fig, ax = plt.subplots(figsize=(10, 10))

def plot_normal(ax, incident_point, mirror_angle):
    normal_length = 0.5
    normal_angle = np.radians(mirror_angle + 90)
    normal_x = [incident_point[0], incident_point[0] + normal_length * np.cos(normal_angle)]
    normal_y = [incident_point[1], incident_point[1] + normal_length * np.sin(normal_angle)]
    ax.plot(normal_x, normal_y, 'g:', linewidth=1)

def plot_mirror(ax, params):
    incident_point = (params['x_pos'], params['y_pos'])
    (x_i, y_i), (x_r, y_r) = calculate_reflection(
        incident_point,
        params['incident_angle'],
        params['angle']
    )
    
    if 'Rayon incident' not in [line.get_label() for line in ax.get_lines()]:
        ax.plot([x_i, incident_point[0]], [y_i, incident_point[1]], 'b-', label='Rayon incident')
    else:
        ax.plot([x_i, incident_point[0]], [y_i, incident_point[1]], 'b-')
    
    if 'Rayon réfléchi' not in [line.get_label() for line in ax.get_lines()]:
        ax.plot([incident_point[0], x_r], [incident_point[1], y_r], 'r--', label='Rayon réfléchi')
    else:
        ax.plot([incident_point[0], x_r], [incident_point[1], y_r], 'r--')
    
    mirror_length = 1
    mirror_rad = np.radians(params['angle'])
    mirror_x = [incident_point[0] - mirror_length * np.cos(mirror_rad),
                incident_point[0] + mirror_length * np.cos(mirror_rad)]
    mirror_y = [incident_point[1] - mirror_length * np.sin(mirror_rad),
                incident_point[1] + mirror_length * np.sin(mirror_rad)]
    ax.plot(mirror_x, mirror_y, 'k-', linewidth=2)
    
    plot_normal(ax, incident_point, params['angle'])

for params in mirror_params:
    plot_mirror(ax, params)

ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.grid(True)
ax.set_aspect('equal')
ax.set_xlabel('X')
ax.set_ylabel('Y')

handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())

st.pyplot(fig)

st.write("### Paramètres des miroirs")
for i, params in enumerate(mirror_params):
    st.write(f"### Miroir {i+1}")
    st.write(f"- Position: ({params['x_pos']:.1f}, {params['y_pos']:.1f})")
    st.write(f"- Angle du miroir: {params['angle']}°")
    st.write(f"- Angle d'incidence: {params['incident_angle']}°")