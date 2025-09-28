import { useState } from "react";

export const FormularioRegistro = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        confirmPassword: '',
    });

    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
        setError('');
        setSuccess('');
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!formData.email || !formData.password || !formData.confirmPassword) {
            setError('Por favor completa todos los campos.');
            return;
        }
        if (formData.password !== formData.confirmPassword) {
            setError('Las contraseñas no coinciden.');
            return;
        }
        setSuccess('¡Registro exitoso! Bienvenido/a.');
        setFormData({ email: '', password: '', confirmPassword: '' });
    };

    return (
        <div className="min-vh-100 d-flex align-items-center justify-content-center bg-light">
            <div className="card shadow-lg border-0 p-4 rounded-4 bg-light-pink" style={{ maxWidth: '500px', width: '100%' }}>
                <h2 className="text-center mb-4 text-primary fw-bold">Crear cuenta</h2>

                {error && <div className="alert alert-danger text-center">{error}</div>}
                {success && <div className="alert alert-success text-center">{success}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="mb-3 position-relative">
                        <i className="fa-solid fa-at icon-inside-input"></i>
                        <input
                            type="email"
                            name="email"
                            className="form-control ps-5"
                            placeholder="Correo electrónico"
                            value={formData.email}
                            onChange={handleChange}
                        />
                    </div>

                    <div className="mb-3 position-relative">
                        <i className="fa-solid fa-lock icon-inside-input"></i>
                        <input
                            type="password"
                            name="password"
                            className="form-control ps-5"
                            placeholder="Contraseña"
                            value={formData.password}
                            onChange={handleChange}
                        />
                    </div>

                    <div className="mb-4 position-relative">
                        <i className="fa-solid fa-lock icon-inside-input"></i>
                        <input
                            type="password"
                            name="confirmPassword"
                            className="form-control ps-5"
                            placeholder="Confirmar contraseña"
                            value={formData.confirmPassword}
                            onChange={handleChange}
                        />
                    </div>

                    <button type="submit" className="btn btn-pink w-100 fw-bold rounded-pill">
                        Registrarme
                    </button>
                </form>

                <p className="mt-4 text-center text-muted">
                    ¿Ya tienes cuenta? <a href="/login" className="text-decoration-none text-black fw-semibold">Inicia sesión</a>
                </p>
            </div>
        </div>
    );
};