import { Link } from "react-router-dom";

export const Footer = () => (
	<footer className="footer mt-auto py-4 bg-footer text-dark">
		<div className="container">
			<div className="row justify-content-center text-start align-items-start text-md-start text-center ps-lg-5">

				<div className="col-md-4 d-flex flex-column align-items-md-start align-items-center mb-4">
					<img className="img-fluid logo-navbar mb-1" src="src/front/assets/img/wild_and_glow_logo_transparent.png" alt="logo" />
					<p className="mb-1">Síguenos en:</p>
					<ul className="list-unstyled">
						<li className="d-flex align-items-center mb-2">
							<a href="https://www.tiktok.com/@wildglow.shop?_t=ZN-8yH7VKwk3ny&_r=1" className="me-2 d-flex align-items-center text-decoration-none">
								<i className="fa-brands fa-tiktok icon-tiktok fs-5"></i>
							</a>
							<span>wildglow.shop</span>
						</li>
						<li className="d-flex align-items-center">
							<a href="https://www.instagram.com/wildglow.shop/?igsh=MXc2aGJscGR2dWg5Mw%3D%3D&utm_source=qr#" className="me-2 d-flex align-items-center text-decoration-none">
								<i className="fa-brands fa-instagram icon-instagram fs-5"></i>
							</a>
							<span>wildglow.shop</span>
						</li>
					</ul>
				</div>

				<div className="col-md-4 d-flex flex-column align-items-md-start align-items-center mb-4">
					<p className="fw-bold mb-2">Información</p>
					<ul className="list-unstyled ps-0">
						<li className="mb-1">Sobre Nosotros</li>
						<li>Política de envío y devoluciones</li>
						<li>Política de privacidad</li>
						<li>Aviso legal</li>
						<li>Términos de servicio</li>
						<li><Link to={"/politica-de-cookies"}>Política de cookies</Link></li>
					</ul>
				</div>

				<div className="col-md-4 d-flex flex-column align-items-md-start align-items-center mb-4">
					<p className="fw-bold mb-2">Contacto</p>
					<ul className="list-unstyled ps-0">
						<li className="mb-1">Contáctanos</li>
						<li>Se dice de nosotros</li>
					</ul>
				</div>
			</div>

			<hr className="border-dark" />

			<p className="mb-0 text-center text-muted small">
				<i className="fa-solid fa-copyright me-1"></i>
				2025 <strong>Wild & Glow</strong>. Todos los derechos reservados. Hecho con 💖 y mucha cera.
			</p>
		</div>
	</footer>
);
