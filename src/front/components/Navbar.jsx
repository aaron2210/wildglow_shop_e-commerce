import { Link } from "react-router-dom";

export const Navbar = () => {

	return (
		<>
			<nav className="navbar navbar-expand-lg myBg myNav">
				<div className="container-fluid">
					<a className="navbar-brand ms-lg-5 me-lg-5 marca" href="#"><img className="img-fluid logo-navbar" src="src/front/assets/img/wild_and_glow_logo_transparent.png" alt="logo" /></a>
					<button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
						<span className="navbar-toggler-icon"></span>
					</button>
					<div className="collapse navbar-collapse" id="navbarSupportedContent">
						<ul className="navbar-nav me-auto mb-2 mb-lg-0 d-flex align-items-center gap-3">
							<li className="nav-item ms-lg-3">
								<Link className="nav-link active" aria-current="page" to={"/inicio"} >Inicio</Link>
							</li>
							<li className="nav-item dropdown">
								<a className="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
									Productos
								</a>
								<ul className="dropdown-menu">
									<li><a className="dropdown-item" href="#">Velas Aromaticas</a></li>
									<li><a className="dropdown-item" href="#">Quemadores</a></li>
									<li><a className="dropdown-item" href="#">Wax Melts</a></li>
								</ul>
							</li>
							<li className="nav-item">
								<a className="nav-link" href="#">Contacto</a>
							</li>
						</ul>
						<ul className="navbar-nav mb-2 mb-lg-0 d-flex align-items-center gap-3">
							<li className="nav-item">
								<Link to={"/registro"} className="nav-link">Registrar</Link>
							</li>
							<li className="nav-item">
								<a className="nav-link" href="#">Entrar</a>
							</li>
							<li className="nav-item d-flex align-items-center mx-2">
								<div className="barra-divisora"></div>
							</li>
							<li className="nav-item">
								<a className="nav-link" href="#"><i className="fa-solid fa-cart-shopping"></i></a>
							</li>
							<li className="nav-item me-lg-4">
								<button
									className="btn nav-link"
									type="button"
									data-bs-toggle="offcanvas"
									data-bs-target="#offcanvasBusqueda"
									aria-controls="offcanvasBusqueda"
								>
									<i className="fa-solid fa-magnifying-glass"></i>
								</button>
							</li>
						</ul>
					</div>
				</div>

			</nav>

			<div
				className="offcanvas offcanvas-end bg-offcanvas"
				tabIndex="-1"
				id="offcanvasBusqueda"
				aria-labelledby="offcanvasBusquedaLabel"
			>
				<div className="offcanvas-header">
					<h5 className="offcanvas-title" id="offcanvasBusquedaLabel">
						Encuentra tus productos
					</h5>
					<button
						type="button"
						className="btn-close text-reset"
						data-bs-dismiss="offcanvas"
						aria-label="Close"
					></button>
				</div>
				<div className="offcanvas-body">
					<form>
						<div className="mb-3">
							<input
								type="search"
								className="form-control"
								placeholder="Buscar productos..."
								aria-label="Buscar"
							/>
						</div>
						<button type="submit" className="btn w-100 btn-busqueda">
							Buscar
						</button>
					</form>
				</div>
			</div>
		</>
	);
};