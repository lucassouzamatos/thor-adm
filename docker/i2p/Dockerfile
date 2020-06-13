FROM meeh/i2p.i2p

# Allow all addresses in router console
RUN sed -i 's/::1,127.0.0.1/::,0.0.0.0/' /opt/i2p/clients.config && \
	sed -i 's/interface\=127.0.0.1/interface\=0.0.0.0/' /opt/i2p/i2ptunnel.config

