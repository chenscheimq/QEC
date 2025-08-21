# Restored instantaneous-bound plotting helpers
# Paste the contents of this file into a new Jupyter code cell in your notebook
# (adjust variable names/contexts as needed). This re-creates the plotting code
# that computes C_out prefactors and plots the instantaneous leakage bound vs Ep.

import numpy as np
import plotly.graph_objects as go

# Robust scalar extractor
def _scalar(x):
    try:
        return complex(x.full()[0,0])
    except AttributeError:
        return complex(x)

# codespace test (expects S1,S2 to be defined in notebook)
def in_codespace(psi, S1, S2, tol=1e-6):
    s1 = float(np.real(_scalar(psi.dag()*S1*psi)))
    s2 = float(np.real(_scalar(psi.dag()*S2*psi)))
    return (abs(s1-1.0) < tol) and (abs(s2-1.0) < tol)

# C(t): prefactor without Bose factor (spectral + matrix elements only)
# Expects: make_H_func(Ep_val), spectral_amp(omega, lambda_2, platform, model),
#          t_list, n_qubits, PLATFORM, lambda_2 available in notebook scope.
def C_out_prefactor_at_t(t, H_func, S1, S2, n_qubits=3, lambda_2=None, PLATFORM='ibm'):
    Ht = H_func(t)
    evals, evecs = Ht.eigenstates()
    a = evecs[0]; Ea = float(evals[0])

    sm_ops = [tensor([sigmam() if j==i else qeye(2) for j in range(n_qubits)]) for i in range(n_qubits)]
    total = 0.0
    for b_idx in range(1, len(evals)):
        b = evecs[b_idx]
        # skip code-space vectors
        if in_codespace(b, S1, S2):
            continue
        Eb = float(evals[b_idx])
        omega = Eb - Ea
        if omega <= 1e-12:
            continue
        g_amp = spectral_amp(omega, lambda_2, platform=PLATFORM, model=None)
        if g_amp == 0.0:
            continue
        acc = 0.0
        for sm in sm_ops:
            m = _scalar(a.dag()*sm*b)
            acc += float(np.abs(m)**2)
        total += (g_amp**2) * acc
    return float(total)

# Max over t for instantaneous condition
def C_max_for_Ep(Ep_val, make_H_func, t_list, n_qubits=3, lambda_2=None):
    H_fun = make_H_func(Ep_val)
    C_vals = [C_out_prefactor_at_t(t, H_fun, S1, S2, n_qubits=n_qubits, lambda_2=lambda_2, PLATFORM=PLATFORM) for t in t_list]
    return float(np.nanmax(C_vals)) if len(C_vals) else 0.0

# Ep to MHz helper (platform-aware)
def Ep_to_MHz(Ep_val, PLATFORM='ibm'):
    if PLATFORM.lower()=='ibm':
        return (Ep_val/(2*np.pi))/1e6       # rad/s -> MHz
    else:
        return (Ep_val/(2*np.pi))           # rad/µs -> MHz

# Plot function: computes Smax_bound (N(Ep)*max C) and plots vs Ep_vec
def plot_instantaneous_bound(Ep_vec, make_H_func, N_of_Ep_func, t_list, lambda_2, S1, S2, PLATFORM, epsilon_R=0.1, to_freq_units=1.0):
    # Ep_vec: iterable of Ep values in same units as make_H_func expects
    # N_of_Ep_func: function Ep -> Bose factor or prefactor N(Ep) (dimensionless)
    Smax_bound = []
    for Ep in Ep_vec:
        Cmax = C_max_for_Ep(Ep, make_H_func, t_list, n_qubits=3, lambda_2=lambda_2)
        Smax_bound.append(N_of_Ep_func(Ep) * Cmax)
    Smax_bound = np.array(Smax_bound, dtype=float)

    # threshold (units match Smax_bound): ε_R * Ω_max — assume omega_max available in global scope
    S_threshold = epsilon_R * omega_max if 'omega_max' in globals() else epsilon_R

    # Prepare plot
    Ep_MHz_axis = np.array([Ep_to_MHz(e, PLATFORM) for e in Ep_vec])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Ep_MHz_axis, y=Smax_bound*to_freq_units, mode='lines+markers', name='N(Ep) · max_t C'))

    # horizontal threshold
    fig.add_hline(y=S_threshold, line=dict(color='red', dash='dash'), annotation_text=f'ε_R·Ω_max = {S_threshold:.3g}', annotation_position='top left')

    # shaded area below threshold
    ymin = np.nanmin(Smax_bound*to_freq_units)
    ymax = np.nanmax(Smax_bound*to_freq_units)
    fig.add_trace(go.Scatter(x=np.concatenate((Ep_MHz_axis, Ep_MHz_axis[::-1])),
                             y=np.concatenate((np.minimum(Smax_bound*to_freq_units, S_threshold), np.zeros_like(Smax_bound)[::-1] + ymin)),
                             fill='toself', fillcolor='rgba(0,200,0,0.15)', line=dict(color='rgba(0,0,0,0)'), showlegend=False))

    fig.update_layout(title=f'Instantaneous leakage bound vs Ep (Platform={PLATFORM})',
                      xaxis_title='Penalty Ep [MHz]',
                      yaxis_title=f'N(Ep) · max_t C(t) [arb units]',
                      template='plotly_white')
    fig.update_yaxes(range=[0, max(ymax, S_threshold)*1.1])
    fig.show()

# End of restored helpers
