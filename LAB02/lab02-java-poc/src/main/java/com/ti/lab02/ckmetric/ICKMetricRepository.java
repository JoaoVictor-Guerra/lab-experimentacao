package com.ti.lab02.ckmetric;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ICKMetricRepository extends JpaRepository<CKMetric, Long> {
}
