export const Banner = () => {
    return (
        <>
            <div className="container myContainer bg-light-pink rounded-4 mt-5 mb-5 p-4 p-lg-5 shadow">
                <div className="row align-items-center">

                    <div className="col-md-6 text-center text-md-start">
                        <h2 className="fw-bold fs-1 mb-4">
                            Enciende el aroma, <br />
                            <span className="slogan">transforma tu espacio</span>
                        </h2>


                        <div className="d-flex justify-content-center justify-content-md-start align-items-center gap-4 mb-4">
                            <div>
                                <h5 className="fw-bold">30+</h5>
                                <p className="m-0">Productos</p>
                            </div>
                            <div className="vr" style={{ height: '40px' }}></div>
                            <div>
                                <h5 className="fw-bold">100+</h5>
                                <p className="m-0">Clientes</p>
                            </div>
                        </div>


                        <div className="input-group w-80 mx-auto mx-md-0">
                            <input
                                type="text"
                                className="form-control rounded-start-pill"
                                placeholder="¿Qué estás buscando?"
                            />
                            <button className="btn btn-busqueda rounded-end-pill">
                                <i className="fas fa-search"></i>
                            </button>
                        </div>
                    </div>


                    <div className="col-md-6 text-center mt-4 mt-md-0">
                        <img
                            src="src/front/assets/img/quemador.png"
                            alt="quemador"
                            className="img-fluid img-quemador rounded-5 offset-up"
                        />

                        <img src="src/front/assets/img/vela.png" alt="vela"
                            className="img-fluid img-quemador rounded-5 ms-lg-5 mt-3 mt-lg-0 offset-down"
                        />
                    </div>
                </div>
            </div>
        </>
    )
}