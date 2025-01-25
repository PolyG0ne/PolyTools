import streamlit as st
import numpy as np
import plotly.graph_objects as go
from math import radians, degrees, cos, sin, tan, pi

def calculate_reflection(mirror_pos, mirror_angle, light_source):
    # Conversion en radians
    theta = radians(mirror_angle)
    
    # Vecteur normal au miroir
    normal = np.array([cos(theta + pi/2), sin(theta + pi/2)])
    
    # Vecteur incident
    incident = light_source - mirror_pos
    incident = incident / np.linalg.norm(incident)
    
    # Calcul du vecteur réfléchi: R = I - 2(I·N)N
    reflection = incident - 2 * np.dot(incident, normal) * normal
    
    return normal, incident, reflection

def create_figure(mirror_pos, mirror_angle, light_source, scale=100):
    # Calcul des vecteurs
    normal, incident, reflection = calculate_reflection(mirror_pos, mirror_angle, light_source)
    
    # Création du miroir
    theta = radians(mirror_angle)
    mirror_start = mirror_pos + np.array([-cos(theta), -sin(theta)]) * scale
    mirror_end = mirror_pos + np.array([cos(theta), sin(theta)]) * scale
    
    # Création de la figure Plotly
    fig = go.Figure()
    
    # Miroir
    fig.add_trace(go.Scatter(x=[mirror_start[0], mirror_end[0]], 
                            y=[mirror_start[1], mirror_end[1]],
                            mode='lines',
                            name='Miroir',
                            line=dict(color='black', width=2)))
    
    # Rayon incident
    fig.add_trace(go.Scatter(x=[light_source[0], mirror_pos[0]], 
                            y=[light_source[1], mirror_pos[1]],
                            mode='lines+text',
                            name='Rayon incident',
                            line=dict(color='red', width=2)))
    
    # Rayon réfléchi
    reflected_end = mirror_pos + reflection * scale
    fig.add_trace(go.Scatter(x=[mirror_pos[0], reflected_end[0]], 
                            y=[mirror_pos[1], reflected_end[1]],
                            mode='lines',
                            name='Rayon réfléchi',
                            line=dict(color='blue', width=2)))
    
    # Normale
    normal_end = mirror_pos + normal * (scale/2)
    fig.add_trace(go.Scatter(x=[mirror_pos[0], normal_end[0]], 
                            y=[mirror_pos[1], normal_end[1]],
                            mode='lines',
                            name='Normale',
                            line=dict(color='green', dash='dash', width=2)))
    
    # Configuration de la mise en page
    fig.update_layout(
        title="Simulation de la Réflexion Spéculaire",
        xaxis_title="X",
        yaxis_title="Y",
        showlegend=True,
        width=800,
        height=600,
        xaxis=dict(range=[-scale, scale], scaleanchor="y", scaleratio=1),
        yaxis=dict(range=[-scale, scale])
    )
    
    return fig

def main():
    st.title("Simulation de la Réflexion Spéculaire")
    
    # Paramètres du miroir
    st.sidebar.header("Paramètres")
    mirror_angle = st.sidebar.slider("Angle du miroir (degrés)", -90, 90, 0)
    source_x = st.sidebar.slider("Position X source lumineuse", -80, 80, -50)
    source_y = st.sidebar.slider("Position Y source lumineuse", -80, 80, 50)
    
    # Position du miroir fixe au centre
    mirror_pos = np.array([0, 0])
    light_source = np.array([source_x, source_y])
    
    # Calcul et affichage
    fig = create_figure(mirror_pos, mirror_angle, light_source)
    st.plotly_chart(fig)
    
    # Calcul des angles
    normal, incident, reflection = calculate_reflection(mirror_pos, mirror_angle, light_source)
    angle_incident = degrees(np.arccos(np.dot(-incident, normal)))
    angle_reflection = degrees(np.arccos(np.dot(reflection, normal)))
    
    # Affichage des informations
    st.sidebar.markdown("### Informations")
    st.sidebar.write(f"Angle d'incidence: {angle_incident:.1f}°")
    st.sidebar.write(f"Angle de réflexion: {angle_reflection:.1f}°")

if __name__ == "__main__":
    main()