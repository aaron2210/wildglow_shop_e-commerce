export const Carrusel = () => {
    return (
        <div id="carouselExampleIndicators" className="carousel slide carousel-fade" data-bs-ride="carousel" data-bs-interval="4000" data-bs-pause="hover">
            <div className="carousel-indicators">
                <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" className="active" aria-current="true" aria-label="Slide 1"></button>
                <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1" aria-label="Slide 2"></button>
                <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2" aria-label="Slide 3"></button>
            </div>

            <div className="carousel-inner">
                <div className="carousel-item active">
                    <div className="carousel-overlay-wrapper position-relative">
                        <img src="src/front/assets/img/Oferta de Verano_ Cera Aromática.png" alt="..." />
                        <div className="carousel-overlay position-absolute top-0 start-0 w-100 h-100"></div>
                    </div>
                </div>

                <div className="carousel-item">
                    <div className="carousel-overlay-wrapper position-relative">
                        <img src="src/front/assets/img/Productos aromáticos personalizados y coloridos.png" alt="..." />
                        <div className="carousel-overlay position-absolute top-0 start-0 w-100 h-100"></div>
                    </div>
                </div>

                <div className="carousel-item">
                    <div className="carousel-overlay-wrapper position-relative">
                        <img src="https://alfabetajuega.com/hero/2025/03/un-nuevo-anime-de-digimon-ha-sido-anunciado.jpg?width=1200" alt="..." />
                        <div className="carousel-overlay position-absolute top-0 start-0 w-100 h-100"></div>
                    </div>
                </div>
            </div>

            <button className="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
                <span className="carousel-control-prev-icon" aria-hidden="true"></span>
                <span className="visually-hidden">Anterior</span>
            </button>
            <button className="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
                <span className="carousel-control-next-icon" aria-hidden="true"></span>
                <span className="visually-hidden">Siguiente</span>
            </button>
        </div>
    )
}